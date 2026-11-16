from config import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    instituicao = db.Column(db.String(255), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    trabalhos = db.relationship("Trabalho", back_populates="usuario")
