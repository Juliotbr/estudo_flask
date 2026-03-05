from flask import Flask, render_template, request, redirect
from models import db, Nota  # Importa o banco de dados e a classe Nota do arquivo models.py

app = Flask(__name__)

# Configurações do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

# Conecta o banco de dados
db.init_app(app)

# Garante que a tabela exista
with app.app_context():
    db.create_all()

# A Rota principal
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        texto_digitado = request.form['conteudo']
        
        nova_nota = Nota(conteudo=texto_digitado)
        db.session.add(nova_nota)
        db.session.commit()
        
        return redirect('/')
    
    todas_as_notas = Nota.query.all()
    return render_template('index.html', notas=todas_as_notas)

# Rota para deletar uma anotação específica pelo ID dela
@app.route('/deletar/<int:id>')
def deletar(id):
    # Busca a nota no banco de dados. Se não achar, dá erro 404
    nota_para_deletar = Nota.query.get_or_404(id)
    
    # Manda o banco deletar e salva a alteração
    db.session.delete(nota_para_deletar)
    db.session.commit()
    
    # Volta para a página inicial
    return redirect('/')

# Rota para editar uma anotação existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Busca a nota pelo ID
    nota_para_editar = Nota.query.get_or_404(id)
    
    if request.method == 'POST':
        # Pega o texto novo do formulário e atualiza o banco
        nota_para_editar.conteudo = request.form['conteudo']
        db.session.commit()
        return redirect('/')
    
    # Se for apenas GET, renderiza a página de edição passando a nota atual
    return render_template('editar.html', nota=nota_para_editar)

if __name__ == '__main__':
    app.run(debug=True)