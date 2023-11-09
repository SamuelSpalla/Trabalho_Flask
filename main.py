import mysql.connector
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='24534152',
    database='Aula_13_10',
    
)


app = Flask(__name__)
app.config['SECRET_KEY'] = "PALAVRA-SECRETA"
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:24534152@localhost/Aula_13_10'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class usuarios(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def __init__(self, id, username, senha):
        self.id = id
        self.username = username
        self.senha = senha
        
@login_manager.user_loader
def load_user(user_id):
    return usuarios.query.get(int(user_id))
        
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        user = usuarios.query.filter_by(username=username).first()
        if user and user.senha == senha:
            login_user(user)
            return redirect('/home')
        else:
            flash("Credenciais de login inválidas. Tente novamente.")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



#-------------------------------------------------------      
class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
class Cargos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'))
    setor = db.relationship('Setor', backref='cargos')    
    
class Funcionarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primeiro_nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    status_funcionario = db.Column(db.Boolean, nullable=False)
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'))
    setor = db.relationship('Setor', backref='funcionarios')
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargos.id'))
    cargo = db.relationship('Cargos', backref='funcionarios')
        
#-------------------------------------------------------

@app.route('/home')
@login_required
def home():
    employees = Funcionarios.query.all()
    cargos = Cargos.query.all()
    setores = Setor.query.all()
    return render_template('home.html', employees=employees, setores=setores, cargos=cargos)

@app.route('/setor')
@login_required
def setor():
    nome = 'Setor'
    return render_template('pages/setor.html', nome=nome)

@app.route('/funcionario')
@login_required
def funcionario():
    cargos = Cargos.query.all()
    setores = Setor.query.all()
    nome = 'Funcionário'
    return render_template('pages/funcionario.html', nome=nome, setores=setores, cargos=cargos)

@app.route('/cargo')
@login_required
def cargo():
    nome = 'Cargo'
    return render_template('pages/cargo.html', nome=nome)

def insert_data(table_name, data):
    my_cursor = mydb.cursor()
    columns = ', '.join(data.keys())
    values = ', '.join([f"'{value}'" for value in data.values()])
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    my_cursor.execute(sql)
    mydb.commit()
    flash(f"Registro em {table_name} criado com sucesso.")

@app.route('/post_setor', methods=['POST'])
def create_setor():
    setor_data = {
        'nome': request.form.get('nome_setor'),
    }
    insert_data('setor', setor_data)
    return redirect('/setor')

@app.route('/post_funcionario', methods=['POST'])
def create_employee():
    status_funcionario = 1 if request.form.get('status_funcionario') == 'on' else 0
    employee_data = {
        'primeiro_nome': request.form.get('primeiro_nome'),
        'sobrenome': request.form.get('sobrenome'),
        'data_admissao': request.form.get('data_admissao'),
        'status_funcionario': status_funcionario,
        'id_setor': request.form.get('id_setor'),
        'id_cargo': request.form.get('id_cargo')
    }
    
    if 'status_funcionario' not in request.form:
        employee_data['status_funcionario'] = 0
        
    insert_data('funcionarios', employee_data)
    return redirect('/funcionario')

@app.route('/post_cargo', methods=['POST'])
def create_job():
    job_data = {
        'nome': request.form.get('nome'),
        'id_setor': request.form.get('id_setor')
    }
    insert_data('cargos', job_data)
    return redirect('/cargo')



if __name__ == "__main__":
     app.run(debug=True)