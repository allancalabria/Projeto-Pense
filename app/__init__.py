import secrets
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, g, render_template, session
from sqlalchemy import inspect, text
from config import db, Config
from app.usuarios import bp as usuarios_bp
from app.usuarios.models import Usuario
from app.trabalhos import bp as trabalhos_bp
from app.trabalhos.models import Trabalho

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
app.register_blueprint(usuarios_bp)

@app.before_request
def load_logged_in_user():
    user_id = session.get("usuario_id")
    g.current_user = db.session.get(Usuario, user_id) if user_id else None


@app.context_processor
def inject_template_helpers():
    def csrf_token():
        if "_csrf_token" not in session:
            session["_csrf_token"] = secrets.token_urlsafe(32)
        return session["_csrf_token"]

    return {"current_user": g.get("current_user"), "csrf_token": csrf_token}


@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_interno_servidor(error):
    db.session.rollback()
    app.logger.error('Erro interno do servidor: %s', error)
    return render_template('500.html'), 500
