from datetime import datetime
from caminhaoagenda import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome_usuario = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(60), nullable=False)
    empresas = database.relationship('Empresa', backref='usuario', lazy=True)
    pedidos = database.relationship('Pedido', backref='usuario', lazy=True)

class Empresa(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cnpj = database.Column(database.String(14), unique=True, nullable=False)
    nome = database.Column(database.String(100), nullable=False)
    nome_fantasia = database.Column(database.String(100), nullable=False)
    endereco = database.Column(database.String(255), nullable=False)
    cidade = database.Column(database.String(100), nullable=False)
    estado = database.Column(database.String(50), nullable=False)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    # Adicione outros campos necessários para a empresa

class Caminhao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    placa = database.Column(database.String(10), unique=True, nullable=False)
    empresa_id = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    empresa = database.relationship('Empresa', backref='caminhoes')
    # Adicione outros campos necessários para o caminhão

class Motorista(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cpf = database.Column(database.String(11), unique=True, nullable=False)
    nome = database.Column(database.String(100), nullable=False)
    telefone = database.Column(database.String(20), nullable=True)
    empresa_id = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    empresa = database.relationship('Empresa', backref='motoristas')
    # Adicione outros campos necessários para o motorista

class Pedido(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    hora_chegada = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    hora_partida = database.Column(database.DateTime, nullable=True)
    empresa_id = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    empresa = database.relationship('Empresa', backref='pedidos')
    caminhao_id = database.Column(database.Integer, database.ForeignKey('caminhao.id'), nullable=False)
    caminhao = database.relationship('Caminhao', backref='pedidos')
    motorista_id = database.Column(database.Integer, database.ForeignKey('motorista.id'), nullable=False)
    motorista = database.relationship('Motorista', backref='pedidos')
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    # Adicione outros campos necessários para o pedido


