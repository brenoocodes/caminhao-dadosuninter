from datetime import datetime
from flask_login import UserMixin
from caminhaoagenda import database, login_manager

# Define o modelo da tabela Usuario
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    password = database.Column(database.String(60), nullable=False)

# Define o modelo da tabela Empresa
class Empresa(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cnpj = database.Column(database.String(14), unique=True, nullable=False)
    nome = database.Column(database.String(100), nullable=False)
    nome_fantasia = database.Column(database.String(100), nullable=False)
    endereco = database.Column(database.String(200), nullable=False)
    telefones = database.Column(database.String(50), nullable=False)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    usuario = database.relationship('Usuario', backref='empresas', lazy=True)

# Define o modelo da tabela Caminhao
class Caminhao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    placa = database.Column(database.String(10), unique=True, nullable=False)
    empresa_id = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    empresa = database.relationship('Empresa', backref='caminhoes', lazy=True)

# Define o modelo da tabela Motorista
class Motorista(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_completo = database.Column(database.String(100), nullable=False)
    cpf = database.Column(database.String(11), unique=True, nullable=False)
    telefone = database.Column(database.String(20), nullable=False)

# Define o modelo da tabela Agendamento
class Agendamento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data_chegada = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    horario_chegada = database.Column(database.Time, nullable=False)
    tempo_estimado = database.Column(database.Integer, nullable=False)
    empresa_id = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    empresa = database.relationship('Empresa', backref='agendamentos', lazy=True)
    caminhao_id = database.Column(database.Integer, database.ForeignKey('caminhao.id'), nullable=False)
    caminhao = database.relationship('Caminhao', backref='agendamentos', lazy=True)
    motorista_id = database.Column(database.Integer, database.ForeignKey('motorista.id'), nullable=False)
    motorista = database.relationship('Motorista', backref='agendamentos', lazy=True)

# Implementa a função necessária para o LoginManager
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))



