# main.py
from flask import Flask, render_template, request, redirect, url_for, flash
import re
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Defina uma chave secreta para o uso do flash

# Função para criar a tabela no banco de dados, se não existir
def criar_tabela():
    conn = sqlite3.connect('caminhoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj TEXT,
            nome_empresa TEXT,
            placa_caminhao TEXT,
            nome_motorista TEXT,
            cpf_motorista TEXT,
            telefone_empresa TEXT,
            data_chegada DATE,
            horario_previsto TIME,
            tempo_carregamento INTEGER,
            horario_saida_previsto TIME
        )
    ''')
    conn.commit()
    conn.close()

# Rota para a página inicial
@app.route('/')
def index():
    criar_tabela()
    conn = sqlite3.connect('caminhoes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos')
    pedidos = cursor.fetchall()
    conn.close()
    return render_template('index.html', pedidos=pedidos)

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        cnpj = request.form['cnpj']
        nome_empresa = request.form['nome_empresa']
        placa_caminhao = request.form['placa_caminhao']
        nome_motorista = request.form['nome_motorista']
        cpf_motorista = request.form['cpf_motorista']
        telefone_empresa = request.form['telefone_empresa']
        data_chegada = request.form['data_chegada']
        horario_previsto = request.form['horario_previsto']
        tempo_carregamento = request.form['tempo_carregamento']

        # Tratamento de erros
        if not re.match(r'\d{14}', cnpj):
            flash("CNPJ inválido. Favor inserir um CNPJ válido.")
            return redirect(url_for('cadastro'))

        if not re.match(r'\d{11}', cpf_motorista):
            flash("CPF do motorista inválido. Favor inserir um CPF válido.")
            return redirect(url_for('cadastro'))

        if not re.match(r'\d{11}', telefone_empresa):
            flash("Telefone da empresa inválido. Favor inserir um telefone válido.")
            return redirect(url_for('cadastro'))

        # Formatação dos dados
        cnpj_formatado = formatar_cnpj(cnpj)
        cpf_motorista_formatado = formatar_cpf(cpf_motorista)
        telefone_empresa_formatado = formatar_telefone(telefone_empresa)

        # Cálculo do horário de saída previsto
        horario_saida_previsto = calcular_horario_saida(data_chegada, horario_previsto, tempo_carregamento)

        # Inserir no banco de dados
        conn = sqlite3.connect('caminhoes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pedidos (
                cnpj, nome_empresa, placa_caminhao, nome_motorista, cpf_motorista, 
                telefone_empresa, data_chegada, horario_previsto, tempo_carregamento, horario_saida_previsto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cnpj_formatado, nome_empresa, placa_caminhao, nome_motorista, cpf_motorista_formatado,
              telefone_empresa_formatado, data_chegada, horario_previsto, tempo_carregamento, horario_saida_previsto))
        conn.commit()
        conn.close()

        flash("Pedido cadastrado com sucesso!")
        return redirect(url_for('index'))

    return render_template('cadastro.html')

# Rota para a página de alteração
@app.route('/alterar/<int:id>', methods=['GET', 'POST'])
def alteracao(id):
    criar_tabela()
    conn = sqlite3.connect('caminhoes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos WHERE id = ?', (id,))
    pedido = cursor.fetchone()
    conn.close()

    if pedido is None:
        flash("Pedido não encontrado.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        cnpj = request.form['cnpj']
        nome_empresa = request.form['nome_empresa']
        placa_caminhao = request.form['placa_caminhao']
        nome_motorista = request.form['nome_motorista']
        cpf_motorista = request.form['cpf_motorista']
        telefone_empresa = request.form['telefone_empresa']
        data_chegada = request.form['data_chegada']
        horario_previsto = request.form['horario_previsto']
        tempo_carregamento = request.form['tempo_carregamento']

        # Tratamento de erros
        if not re.match(r'\d{14}', cnpj):
            flash("CNPJ inválido. Favor inserir um CNPJ válido.")
            return redirect(url_for('alteracao', id=id))

        if not re.match(r'\d{11}', cpf_motorista):
            flash("CPF do motorista inválido. Favor inserir um CPF válido.")
            return redirect(url_for('alteracao', id=id))

        if not re.match(r'\d{11}', telefone_empresa):
            flash("Telefone da empresa inválido. Favor inserir um telefone válido.")
            return redirect(url_for('alteracao', id=id))

        # Formatação dos dados
        cnpj_formatado = formatar_cnpj(cnpj)
        cpf_motorista_formatado = formatar_cpf(cpf_motorista)
        telefone_empresa_formatado = formatar_telefone(telefone_empresa)

        # Cálculo do horário de saída previsto
        horario_saida_previsto = calcular_horario_saida(data_chegada, horario_previsto, tempo_carregamento)

        # Atualizar no banco de dados
        conn = sqlite3.connect('caminhoes.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pedidos SET 
            cnpj=?, nome_empresa=?, placa_caminhao=?, nome_motorista=?, cpf_motorista=?, 
            telefone_empresa=?, data_chegada=?, horario_previsto=?, tempo_carregamento=?, horario_saida_previsto=?
            WHERE id=?
        ''', (cnpj_formatado, nome_empresa, placa_caminhao, nome_motorista, cpf_motorista_formatado,
              telefone_empresa_formatado, data_chegada, horario_previsto, tempo_carregamento, horario_saida_previsto, id))
        conn.commit()
        conn.close()

        flash("Pedido alterado com sucesso!")
        return redirect(url_for('index'))

    return render_template('alterar.html', pedido=pedido)

# Função para calcular o horário de saída previsto
def calcular_horario_saida(data_chegada, horario_previsto, tempo_carregamento):
    dt_chegada = datetime.strptime(f'{data_chegada} {horario_previsto}', '%Y-%m-%d %H:%M')
    dt_saida_prevista = dt_chegada + timedelta(minutes=int(tempo_carregamento))
    return dt_saida_prevista.strftime('%H:%M')

# Função para formatar o CNPJ
def formatar_cnpj(cnpj):
    return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'

# Função para formatar o CPF
def formatar_cpf(cpf):
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

# Função para formatar o telefone
def formatar_telefone(telefone):
    return f'({telefone[:2]}) 9 {telefone[2:6]}-{telefone[6:]}'

if __name__ == '__main__':
    app.run(debug=True)
