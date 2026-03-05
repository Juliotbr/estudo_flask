from flask import Flask, render_template, request, redirect
from models import db, Nota, Categoria, Equipamento 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db.init_app(app)

# Garante que o banco exista e cria os dados iniciais
with app.app_context():
    db.create_all()
    
    # Se não existir nenhuma categoria no banco, ele cria essas opções padrão:
    if not Categoria.query.first():
        db.session.add_all([
            Categoria(nome='Estudos Univesp'),
            Categoria(nome='Projetos Maker'),
            Categoria(nome='Planos de Aula')
        ])
        db.session.add_all([
            Equipamento(nome='Kit Arduino'),
            Equipamento(nome='Chromebook'),
            Equipamento(nome='Componentes Eletrônicos')
        ])
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        texto = request.form['conteudo']
        cat_id = request.form['categoria_id']
        
        # O equipamento é opcional. Se vier vazio (""), transformamos em None (Nulo)
        eq_id = request.form.get('equipamento_id')
        if eq_id == "":
            eq_id = None
        
        # Salva a nota já amarrada aos IDs das outras tabelas!
        nova_nota = Nota(conteudo=texto, categoria_id=cat_id, equipamento_id=eq_id)
        db.session.add(nova_nota)
        db.session.commit()
        return redirect('/')
    
    # Busca tudo no banco para mandar para a tela
    todas_as_notas = Nota.query.all()
    todas_as_categorias = Categoria.query.all()
    todos_os_equipamentos = Equipamento.query.all()
    
    return render_template('index.html', 
                           notas=todas_as_notas, 
                           categorias=todas_as_categorias, 
                           equipamentos=todos_os_equipamentos)

# Rota de deletar (continua igual)
@app.route('/deletar/<int:id>')
def deletar(id):
    nota_para_deletar = Nota.query.get_or_404(id)
    db.session.delete(nota_para_deletar)
    db.session.commit()
    return redirect('/')

# ROTA 1: Tela de Gerenciar Categorias (Lista e Cria)
@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if request.method == 'POST':
        novo_nome = request.form['nome_categoria']
        nova_categoria = Categoria(nome=novo_nome)
        db.session.add(nova_categoria)
        db.session.commit()
        return redirect('/categorias')
    
    todas_as_categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=todas_as_categorias)

# ROTA 2: Deletar a Categoria
@app.route('/deletar_categoria/<int:id>')
def deletar_categoria(id):
    categoria_para_deletar = Categoria.query.get_or_404(id)
    
    # PROTEÇÃO DO BANCO: Primeiro deletamos todas as notas vinculadas a esta categoria
    Nota.query.filter_by(categoria_id=id).delete()
    
    # Depois, deletamos a categoria em si
    db.session.delete(categoria_para_deletar)
    db.session.commit()
    
    return redirect('/categorias')

# ROTAS DE EQUIPAMENTOS
@app.route('/equipamentos', methods=['GET', 'POST'])
def equipamentos():
    if request.method == 'POST':
        novo_nome = request.form['nome_equipamento']
        novo_equipamento = Equipamento(nome=novo_nome)
        db.session.add(novo_equipamento)
        db.session.commit()
        return redirect('/equipamentos')
    
    todos_os_equipamentos = Equipamento.query.all()
    return render_template('equipamentos.html', equipamentos=todos_os_equipamentos)

@app.route('/deletar_equipamento/<int:id>')
def deletar_equipamento(id):
    equipamento_para_deletar = Equipamento.query.get_or_404(id)
    
    # PROTEÇÃO INTELIGENTE: Em vez de deletar as notas, apenas removemos o equipamento delas
    notas_vinculadas = Nota.query.filter_by(equipamento_id=id).all()
    for nota in notas_vinculadas:
        nota.equipamento_id = None  # A nota sobrevive, mas fica "sem equipamento"
        
    db.session.delete(equipamento_para_deletar)
    db.session.commit()
    return redirect('/equipamentos')

# ROTA DE EDITAR A NOTA
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    nota = Nota.query.get_or_404(id)
    
    if request.method == 'POST':
        # Atualiza o texto, a categoria e o equipamento
        nota.conteudo = request.form['conteudo']
        nota.categoria_id = request.form['categoria_id']
        
        eq_id = request.form.get('equipamento_id')
        nota.equipamento_id = None if eq_id == "" else eq_id
        
        db.session.commit()
        return redirect('/')
    
    # Busca as listas para montar os menus Dropdown na tela de edição
    categorias = Categoria.query.all()
    equipamentos = Equipamento.query.all()
    return render_template('editar.html', nota=nota, categorias=categorias, equipamentos=equipamentos)

if __name__ == '__main__':
    app.run(debug=True)