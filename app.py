import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.middleware.proxy_fix import ProxyFix
from config import db, Config
from models import Trabalho

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Rota do Dashboard (Página Inicial)
@app.route('/')
def dashboard():
    trabalhos = Trabalho.query.all()
    return render_template('dashboard.html', trabalhos=trabalhos)


# Rota do Formulário
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        instituicao = request.form.get('instituicao')
        modalidade = request.form.get('modalidade')
        resumo = request.form.get('resumo')

        if not titulo or not autor or not instituicao or not modalidade or not resumo:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('form'))

        try:
            novo_trabalho = Trabalho(
                titulo=titulo, 
                autor=autor, 
                instituicao=instituicao, 
                modalidade=modalidade, 
                resumo=resumo
            )
            db.session.add(novo_trabalho)
            db.session.commit()
            flash("Trabalho cadastrado com sucesso!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro ao cadastrar o trabalho: {e}", exc_info=True)
            flash('Erro ao cadastrar o trabalho.', 'danger')
            return redirect(url_for('form'))
            
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
