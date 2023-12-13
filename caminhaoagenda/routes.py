from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from caminhaoagenda import app, database, bcrypt
from caminhaoagenda.forms import (
    CadastroEmpresaForm, CadastroCaminhaoForm, CadastroMotoristaForm, CadastroAgendamentoForm,
    AlterarEmpresaForm, AlterarCaminhaoForm, AlterarMotoristaForm, AlterarAgendamentoForm,
    FormCriarConta, FormLogin, FormRecuperarSenha, FormEditarPerfil
)
from caminhaoagenda.models import Empresa, Caminhao, Motorista, Agendamento, Usuario

@app.route('/')
def home():
    return render_template('home.html', title='Home')

# Rotas para cadastro e listagem de empresas
@app.route('/cadastrar_empresa', methods=['GET', 'POST'])
@login_required
def cadastrar_empresa():
    form = CadastroEmpresaForm()

    if form.validate_on_submit():
        empresa = Empresa(cnpj=form.cnpj.data, nome=form.nome.data, nome_fantasia=form.nome_fantasia.data,
                          endereco=form.endereco.data, telefones=form.telefones.data, usuario=current_user)
        database.session.add(empresa)
        database.session.commit()
        flash('Empresa cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_empresa'))

    return render_template('cadastrar_empresa.html', title='Cadastrar Empresa', form=form)

@app.route('/editar_empresa/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
def editar_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    form = AlterarEmpresaForm()

    if form.validate_on_submit():
        empresa.cnpj = form.cnpj.data
        empresa.nome = form.nome.data
        empresa.nome_fantasia = form.nome_fantasia.data
        empresa.endereco = form.endereco.data
        empresa.telefones = form.telefones.data
        database.session.commit()
        flash('Empresa atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_empresa'))

    elif request.method == 'GET':
        form.cnpj.data = empresa.cnpj
        form.nome.data = empresa.nome
        form.nome_fantasia.data = empresa.nome_fantasia
        form.endereco.data = empresa.endereco
        form.telefones.data = empresa.telefones

    return render_template('editar_empresa.html', title='Editar Empresa', form=form, empresa=empresa)

@app.route('/listar_empresas')
@login_required
def listar_empresas():
    empresas = current_user.empresas
    return render_template('listar_empresas.html', title='Empresas', empresas=empresas)

# Rotas para cadastro e listagem de caminhões
@app.route('/cadastrar_caminhao', methods=['GET', 'POST'])
@login_required
def cadastrar_caminhao():
    form = CadastroCaminhaoForm()
    form.empresa_id.choices = [(empresa.id, empresa.nome_fantasia) for empresa in current_user.empresas]

    if form.validate_on_submit():
        caminhao = Caminhao(placa=form.placa.data, empresa_id=form.empresa_id.data)
        database.session.add(caminhao)
        database.session.commit()
        flash('Caminhão cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_caminhao'))

    return render_template('cadastrar_caminhao.html', title='Cadastrar Caminhão', form=form)

@app.route('/editar_caminhao/<int:caminhao_id>', methods=['GET', 'POST'])
@login_required
def editar_caminhao(caminhao_id):
    caminhao = Caminhao.query.get_or_404(caminhao_id)
    form = AlterarCaminhaoForm()
    form.empresa_id.choices = [(empresa.id, empresa.nome_fantasia) for empresa in current_user.empresas]

    if form.validate_on_submit():
        caminhao.placa = form.placa.data
        caminhao.empresa_id = form.empresa_id.data
        database.session.commit()
        flash('Caminhão atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_caminhao'))

    elif request.method == 'GET':
        form.placa.data = caminhao.placa
        form.empresa_id.data = caminhao.empresa_id

    return render_template('editar_caminhao.html', title='Editar Caminhão', form=form, caminhao=caminhao)

@app.route('/listar_caminhoes')
@login_required
def listar_caminhoes():
    caminhoes = current_user.obter_caminhoes()
    return render_template('listar_caminhoes.html', title='Caminhões', caminhoes=caminhoes)

# Rotas para cadastro e listagem de motoristas
@app.route('/cadastrar_motorista', methods=['GET', 'POST'])
@login_required
def cadastrar_motorista():
    form = CadastroMotoristaForm()

    if form.validate_on_submit():
        motorista = Motorista(nome_completo=form.nome_completo.data, cpf=form.cpf.data, telefone=form.telefone.data)
        database.session.add(motorista)
        database.session.commit()
        flash('Motorista cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_motorista'))

    return render_template('cadastrar_motorista.html', title='Cadastrar Motorista', form=form)

@app.route('/editar_motorista/<int:motorista_id>', methods=['GET', 'POST'])
@login_required
def editar_motorista(motorista_id):
    motorista = Motorista.query.get_or_404(motorista_id)
    form = AlterarMotoristaForm()

    if form.validate_on_submit():
        motorista.nome_completo = form.nome_completo.data
        motorista.cpf = form.cpf.data
        motorista.telefone = form.telefone.data
        database.session.commit()
        flash('Motorista atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_motorista'))

    elif request.method == 'GET':
        form.nome_completo.data = motorista.nome_completo
        form.cpf.data = motorista.cpf
        form.telefone.data = motorista.telefone

    return render_template('editar_motorista.html', title='Editar Motorista', form=form, motorista=motorista)

@app.route('/listar_motoristas')
@login_required
def listar_motoristas():
    motoristas = current_user.obter_motoristas()
    return render_template('listar_motoristas.html', title='Motoristas', motoristas=motoristas)

# Rotas para cadastro e listagem de agendamentos
@app.route('/cadastrar_agendamento', methods=['GET', 'POST'])
@login_required
def cadastrar_agendamento():
    form = CadastroAgendamentoForm()
    form.empresa_id.choices = [(empresa.id, empresa.nome_fantasia) for empresa in current_user.empresas]
    form.caminhao_id.choices = [(caminhao.id, caminhao.placa) for caminhao in current_user.obter_caminhoes()]
    form.motorista_id.choices = [(motorista.id, motorista.nome_completo) for motorista in current_user.obter_motoristas()]

    if form.validate_on_submit():
        agendamento = Agendamento(data_chegada=form.data_chegada.data, horario_chegada=form.horario_chegada.data,
                                  tempo_estimado=form.tempo_estimado.data, empresa_id=form.empresa_id.data,
                                  caminhao_id=form.caminhao_id.data, motorista_id=form.motorista_id.data)
        database.session.add(agendamento)
        database.session.commit()
        flash('Agendamento cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_agendamento'))

    return render_template('cadastrar_agendamento.html', title='Cadastrar Agendamento', form=form)

@app.route('/editar_agendamento/<int:agendamento_id>', methods=['GET', 'POST'])
@login_required
def editar_agendamento(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    form = AlterarAgendamentoForm()
    form.empresa_id.choices = [(empresa.id, empresa.nome_fantasia) for empresa in current_user.empresas]
    form.caminhao_id.choices = [(caminhao.id, caminhao.placa) for caminhao in current_user.obter_caminhoes()]
    form.motorista_id.choices = [(motorista.id, motorista.nome_completo) for motorista in current_user.obter_motoristas()]

    if form.validate_on_submit():
        agendamento.data_chegada = form.data_chegada.data
        agendamento.horario_chegada = form.horario_chegada.data
        agendamento.tempo_estimado = form.tempo_estimado.data
        agendamento.empresa_id = form.empresa_id.data
        agendamento.caminhao_id = form.caminhao_id.data
        agendamento.motorista_id = form.motorista_id.data
        database.session.commit()
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_agendamento'))

    elif request.method == 'GET':
        form.data_chegada.data = agendamento.data_chegada
        form.horario_chegada.data = agendamento.horario_chegada
        form.tempo_estimado.data = agendamento.tempo_estimado
        form.empresa_id.data = agendamento.empresa_id
        form.caminhao_id.data = agendamento.caminhao_id
        form.motorista_id.data = agendamento.motorista_id

    return render_template('editar_agendamento.html', title='Editar Agendamento', form=form, agendamento=agendamento)

@app.route('/listar_agendamentos')
@login_required
def listar_agendamentos():
    agendamentos = current_user.obter_agendamentos()
    return render_template('listar_agendamentos.html', title='Agendamentos', agendamentos=agendamentos)
# Rota para cadastro de usuário
@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = FormCriarConta()

    if form.validate_on_submit():
        hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(username=form.username.data, email=form.email.data, password=hashed_senha)
        database.session.add(usuario)
        database.session.commit()
        flash('Sua conta foi criada! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))

    return render_template('criar_conta.html', title='Criar Conta', form=form)

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = FormLogin()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.password, form.senha.data):
            login_user(usuario, remember=form.lembrar_dados.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Falha no login. Verifique seu e-mail e senha.', 'danger')

    return render_template('login.html', title='Login', form=form)

# Rota para logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Rota para recuperar senha
@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    form = FormRecuperarSenha()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        if usuario:
            flash('Um e-mail de recuperação foi enviado para o seu endereço.', 'info')
            # Lógica para enviar e-mail de recuperação de senha (não implementada aqui)
            return redirect(url_for('login'))
        else:
            flash('E-mail não cadastrado. Crie uma conta antes de recuperar a senha.', 'danger')

    return render_template('recuperar_senha.html', title='Recuperar Senha', form=form)

# routes.py

# ... (outros imports)

# Rota para dados da conta
@app.route('/dados_conta', methods=['GET', 'POST'])
@login_required
def dados_conta():
    form = FormEditarPerfil()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.mudar_senha.data:
            hashed_senha = bcrypt.generate_password_hash(form.nova_senha.data).decode('utf-8')
            current_user.password = hashed_senha
        database.session.commit()
        flash('Dados da conta atualizados com sucesso!', 'success')
        return redirect(url_for('dados_conta'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('dados_conta.html', title='Dados da Conta', form=form)
