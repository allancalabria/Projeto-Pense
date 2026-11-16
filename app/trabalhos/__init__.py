from flask import Blueprint

bp = Blueprint('trabalhos', __name__, template_folder='templates')

from app.trabalhos import routes