from flask import Flask, render_template, request, redirect
from models import db, Nota  # <-- Olha a mágica aqui: importando do seu arquivo!

app = Flask(__name__)

# Configurações do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

# Conecta o banco de dados (que estava isolado) ao nosso aplicativo
db.init_app(app)

# Garante que a tabela exista
with app.app_context():
    db.create_all()

# A nossa Rota principal continua igualzinha
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

if __name__ == '__main__':
    app.run(debug=True)