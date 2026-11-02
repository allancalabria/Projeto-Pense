from config import db
import enum

# class ModalidadeEnum(enum.Enum):
#     ENSINO = "Ensino"
#     PESQUISA = "Pesquisa"
#     EXTENSAO = "Extensão"

class Trabalho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    autor = db.Column(db.String(80), nullable=False)
    instituicao = db.Column(db.String(80), nullable=False)
    modalidade = db.Column(db.String(80), nullable=False)
    resumo = db.Column(db.String(80), nullable=False)

    def __init__(self, titulo, autor, instituicao, modalidade, resumo, **kwargs):
        super().__init__(**kwargs)
        self.titulo = titulo
        self.autor = autor
        self.instituicao = instituicao
        self.modalidade = modalidade
        self.resumo = resumo