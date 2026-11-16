import os
import hmac
import re
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, g, render_template, request, redirect, url_for, flash, session, abort
from sqlalchemy import inspect, text
from werkzeug.security import check_password_hash, generate_password_hash
from config import db, Config
from app.models import Usuario
from app.trabalhos import bp as trabalhos_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    columns = {column["name"] for column in inspect(db.engine).get_columns("trabalho")}
    with db.engine.begin() as connection:
        if "status" not in columns:
            connection.execute(text("ALTER TABLE trabalho ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'Pendente'"))
        if "usuario_id" not in columns:
            connection.execute(text("ALTER TABLE trabalho ADD COLUMN usuario_id INTEGER REFERENCES usuarios(id)"))

app.register_blueprint(trabalhos_bp)

@app.before_request
def load_logged_in_user():
    user_id = session.get("usuario_id")
    g.current_user = db.session.get(Usuario, user_id) if user_id else None


@app.context_processor
def inject_template_helpers():
    def csrf_token():
        if "_csrf_token" not in session:
            import secrets
            session["_csrf_token"] = secrets.token_urlsafe(32)
        return session["_csrf_token"]

    return {"current_user": g.get("current_user"), "csrf_token": csrf_token}


def valid_csrf_token():
    submitted_token = request.form.get("csrf_token", "")
    session_token = session.get("_csrf_token", "")
    return bool(session_token and hmac.compare_digest(submitted_token, session_token))


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.current_user is None:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        if not valid_csrf_token():
            abort(400)

        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        cpf = re.sub(r'\D', '', request.form.get('cpf', ''))
        instituicao = request.form.get('instituicao', '').strip()
        senha = request.form.get('senha', '')

        if not all((nome, email, cpf, instituicao, senha)):
            flash('Preencha todos os campos.', 'danger')
            return redirect(url_for('cadastro'))
        if len(nome) > 160 or len(email) > 254 or len(instituicao) > 255:
            flash('Um ou mais campos excedem o limite permitido.', 'danger')
            return redirect(url_for('cadastro'))
        if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
            flash('Informe um e-mail válido.', 'danger')
            return redirect(url_for('cadastro'))
        if len(cpf) != 11:
            flash('Informe um CPF com 11 números.', 'danger')
            return redirect(url_for('cadastro'))
        if len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'danger')
            return redirect(url_for('cadastro'))
        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.', 'danger')
            return redirect(url_for('cadastro'))
        if Usuario.query.filter_by(cpf=cpf).first():
            flash('Este CPF já está cadastrado.', 'danger')
            return redirect(url_for('cadastro'))

        usuario = Usuario(
            nome=nome,
            email=email,
            cpf=cpf,
            instituicao=instituicao,
            senha_hash=generate_password_hash(senha),
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Entre com seu e-mail e senha.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not valid_csrf_token():
            abort(400)
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            flash('E-mail ou senha incorretos.', 'danger')
            return redirect(url_for('login'))

        session.clear()
        session['usuario_id'] = usuario.id
        flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
        return redirect(url_for('trabalhos.dashboard'))

    return render_template('login.html')


@app.post('/logout')
@login_required
def logout():
    if not valid_csrf_token():
        abort(400)
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('trabalhos.dashboard'))


# Rota para editar dados do Usuário
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        # Verifica a proteção CSRF do formulário
        if not valid_csrf_token():
            abort(400)
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        cpf = re.sub(r'\D', '', request.form.get('cpf', ''))
        instituicao = request.form.get('instituicao', '').strip()
        dados = {
            'nome': nome,
            'email': email,
            'cpf': cpf,
            'instituicao': instituicao
        }

        if not all(dados.values()):
            flash('Preencha todos os campos.', 'danger')
            return render_template('editar_usuario.html', dados=dados)

        if len(nome) > 160 or len(email) > 254 or len(instituicao) > 255:
            flash('Um ou mais campos excedem o limite permitido.', 'danger')
            return render_template('editar_usuario.html', dados=dados)

        if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
            flash('Informe um e-mail válido.', 'danger')
            return render_template('editar_usuario.html', dados=dados)

        if len(cpf) != 11:
            flash('Informe um CPF com 11 números.', 'danger')
            return render_template('editar_usuario.html', dados=dados)

        email_existente = Usuario.query.filter(
            Usuario.email == email,
            Usuario.id != g.current_user.id
        ).first()

        if email_existente:
            flash('Este e-mail já está cadastrado por outro usuário.', 'danger')
            return render_template('editar_usuario.html', dados=dados)

        cpf_existente = Usuario.query.filter(
            Usuario.cpf == cpf,
            Usuario.id != g.current_user.id
        ).first()

        if cpf_existente:
            flash('Este CPF já está cadastrado por outro usuário.', 'danger')
            return render_template('editar_usuario.html', dados=dados)

        try:
            g.current_user.nome = nome
            g.current_user.email = email
            g.current_user.cpf = cpf
            g.current_user.instituicao = instituicao

            db.session.commit()

            flash('Seus dados foram atualizados com sucesso!', 'success')
            return redirect(url_for('trabalhos.dashboard'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(
                'Erro ao atualizar os dados do usuário: %s',
                e,
                exc_info=True
            )
            flash('Não foi possível atualizar seus dados.', 'danger')
            return render_template('editar_usuario.html', dados=dados)

    return render_template('editar_usuario.html', dados=None)


# Rota do Formulário
@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    if request.method == 'POST':
        if not valid_csrf_token():
            abort(400)
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        instituicao = request.form.get('instituicao')
        modalidade = request.form.get('modalidade')
        resumo = request.form.get('resumo')
        if modalidade not in {'Ensino', 'Pesquisa', 'Extensão'}:
            flash('Selecione uma modalidade válida.', 'danger')
            return redirect(url_for('form'))

        if not titulo or not autor or not instituicao or not modalidade or not resumo:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('form'))

        if len(titulo) > 255 or len(autor) > 120 or len(instituicao) > 255 or len(modalidade) > 80:
            flash('Limite de caracteres excedido em um ou mais campos.', 'danger')
            return redirect(url_for('form'))

        try:
            novo_trabalho = Trabalho(
                titulo=titulo, 
                autor=autor, 
                instituicao=instituicao, 
                modalidade=modalidade, 
                resumo=resumo,
                usuario_id=g.current_user.id,
            )
            db.session.add(novo_trabalho)
            db.session.commit()
            flash("Submissão enviada com sucesso!", "success")
            return redirect(url_for('trabalhos.dashboard'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro ao cadastrar o trabalho: {e}", exc_info=True)
            flash('Erro ao cadastrar o trabalho.', 'danger')
            return redirect(url_for('form'))
            
    return render_template('form.html')


@app.get('/admin')
@login_required
def admin():
    trabalhos = Trabalho.query.order_by(Trabalho.id.desc()).all()
    return render_template('admin.html', trabalhos=trabalhos)


@app.post('/admin/<int:trabalho_id>/status')
@login_required
def atualizar_status(trabalho_id):
    if not valid_csrf_token():
        abort(400)
    trabalho = db.get_or_404(Trabalho, trabalho_id)
    novo_status = request.form.get('status')
    if novo_status not in {'Pendente', 'Aprovado', 'Reprovado'}:
        flash('Status inválido.', 'danger')
        return redirect(url_for('admin'))

    trabalho.status = novo_status
    db.session.commit()
    flash('Status do trabalho atualizado.', 'success')
    return redirect(url_for('admin'))


@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_interno_servidor(error):
    db.session.rollback()
    app.logger.error('Erro interno do servidor: %s', error)
    return render_template('500.html'), 500
