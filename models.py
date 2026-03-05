from flask_sqlalchemy import SQLAlchemy

# Cria a ferramenta do banco de dados (ainda "desligada" do app)
db = SQLAlchemy()

# Define a estrutura da nossa tabela
class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)