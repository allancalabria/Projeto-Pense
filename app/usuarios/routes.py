import re
from flask import render_template, request, redirect, url_for, flash, session, abort, g, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from config import db
from app.usuarios import bp
from app.usuarios.models import Usuario
from app.utils import login_required, valid_csrf_token


@bp.route('/cadastro', methods=['GET', 'POST'])
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
            return redirect(url_for('usuarios.cadastro'))
        if len(nome) > 160 or len(email) > 254 or len(instituicao) > 255:
            flash('Um ou mais campos excedem o limite permitido.', 'danger')
            return redirect(url_for('usuarios.cadastro'))
        if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
            flash('Informe um e-mail válido.', 'danger')
            return redirect(url_for('usuarios.cadastro'))
        if len(cpf) != 11:
            flash('Informe um CPF com 11 números.', 'danger')
            return redirect(url_for('usuarios.cadastro'))
        if len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'danger')
            return redirect(url_for('usuarios.cadastro'))
        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.', 'danger')
            return redirect(url_for('usuarios.cadastro'))
        if Usuario.query.filter_by(cpf=cpf).first():
            flash('Este CPF já está cadastrado.', 'danger')
            return redirect(url_for('usuarios.cadastro'))

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
        return redirect(url_for('usuarios.login'))

    return render_template('cadastro.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not valid_csrf_token():
            abort(400)
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            flash('E-mail ou senha incorretos.', 'danger')
            return redirect(url_for('usuarios.login'))

        session.clear()
        session['usuario_id'] = usuario.id
        flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
        return redirect(url_for('trabalhos.dashboard'))

    return render_template('login.html')


@bp.post('/logout')
@login_required
def logout():
    if not valid_csrf_token():
        abort(400)
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('trabalhos.dashboard'))


# Rota para editar dados do Usuário
@bp.route('/perfil/editar', methods=['GET', 'POST'])
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
            current_app.logger.error(
                'Erro ao atualizar os dados do usuário: %s',
                e,
                exc_info=True
            )
            flash('Não foi possível atualizar seus dados.', 'danger')
            return render_template('editar_usuario.html', dados=dados)

    return render_template('editar_usuario.html', dados=None)
