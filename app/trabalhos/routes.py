from flask import render_template
from app.trabalhos.models import Trabalho
from app.trabalhos import bp

# Rota do Dashboard (Página Inicial)
@bp.route('/')
def dashboard():
    trabalhos = Trabalho.query.order_by(Trabalho.id.desc()).all()
    return render_template('dashboard.html', trabalhos=trabalhos)