from caminhaoagenda import app, database
from caminhaoagenda.models import Usuario, Empresa, Caminhao, Motorista, Agendamento

# Cria as tabelas no banco de dados
with app.app_context():
    database.create_all()

print('Banco de dados criado.')
