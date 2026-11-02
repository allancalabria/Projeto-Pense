import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("secret_key") or "chave-secreta-padrao"
    
    # Obtém a URL do banco de dados
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
    
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
