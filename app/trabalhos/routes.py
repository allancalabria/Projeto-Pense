from flask import render_template, request, redirect, url_for, flash, abort, g, current_app
from config import db
from app.trabalhos.models import Trabalho
from app.trabalhos import bp
from app.utils import login_required, valid_csrf_token

# Rota do Dashboard (Página Inicial)
@bp.route('/')
def dashboard():
    trabalhos = Trabalho.query.order_by(Trabalho.id.desc()).all()
    return render_template('dashboard.html', trabalhos=trabalhos)


# Rota do Formulário
@bp.route('/form', methods=['GET', 'POST'])
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
            return redirect(url_for('trabalhos.form'))

        if not titulo or not autor or not instituicao or not modalidade or not resumo:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('trabalhos.form'))

        if len(titulo) > 255 or len(autor) > 120 or len(instituicao) > 255 or len(modalidade) > 80:
            flash('Limite de caracteres excedido em um ou mais campos.', 'danger')
            return redirect(url_for('trabalhos.form'))

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
            current_app.logger.error(f"Erro ao cadastrar o trabalho: {e}", exc_info=True)
            flash('Erro ao cadastrar o trabalho.', 'danger')
            return redirect(url_for('trabalhos.form'))
            
    return render_template('form.html')


@bp.get('/admin')
@login_required
def admin():
    trabalhos = Trabalho.query.order_by(Trabalho.id.desc()).all()
    return render_template('admin.html', trabalhos=trabalhos)


@bp.post('/admin/<int:trabalho_id>/status')
@login_required
def atualizar_status(trabalho_id):
    if not valid_csrf_token():
        abort(400)
    trabalho = db.get_or_404(Trabalho, trabalho_id)
    novo_status = request.form.get('status')
    if novo_status not in {'Pendente', 'Aprovado', 'Reprovado'}:
        flash('Status inválido.', 'danger')
        return redirect(url_for('trabalhos.admin'))

    trabalho.status = novo_status
    db.session.commit()
    flash('Status do trabalho atualizado.', 'success')
    return redirect(url_for('trabalhos.admin'))

