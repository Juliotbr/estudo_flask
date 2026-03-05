from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# TABELA 1: Categoria (Obrigatória para toda nota)
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    # O backref cria uma "ponte" invisível. 
    # Com isso, podemos usar 'categoria.notas' para ver todos os posts dessa categoria.
    notas = db.relationship('Nota', backref='categoria', lazy=True)

# TABELA 2: Equipamento (Opcional na nota)
class Equipamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    # Mesma ponte, mas para os equipamentos.
    notas = db.relationship('Nota', backref='equipamento', lazy=True)

# TABELA 3: A Nota principal (O Post)
class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    
    # CHAVE ESTRANGEIRA OBRIGATÓRIA: nullable=False faz o banco recusar salvar se não tiver categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    
    # CHAVE ESTRANGEIRA OPCIONAL: nullable=True permite que a nota exista sem nenhum equipamento vinculado
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamento.id'), nullable=True)