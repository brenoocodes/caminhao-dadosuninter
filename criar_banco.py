from caminhaoagenda import app, database
from caminhaoagenda.models import Caminhao, Empresa, Motorista, Pedido, Usuario

with app.app_context():
    database.create_all()

print('Banco de dados criado.')

