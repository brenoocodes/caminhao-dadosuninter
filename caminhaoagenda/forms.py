from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from caminhaoagenda.models import Usuario
from flask import render_template, redirect, url_for, flash, request


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError(f'E-mail já cadastrado. Faça o login.')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    mudar_senha = BooleanField('Mudar Senha')
    senha_atual = PasswordField('Senha Atual')
    nova_senha = PasswordField('Nova Senha')
    confirmacao_nova_senha = PasswordField('Confirmação da Nova Senha')

    def validate_email(self, email):
        if email.data != current_user.email:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError(f'E-mail já cadastrado. Escolha outro.')

class FormAlterarSenha(FlaskForm):
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_nova_senha = PasswordField('Confirmação da Nova Senha', validators=[DataRequired(), EqualTo('nova_senha')])

    def validate_senha_atual(self, senha_atual):
        if not current_user.verificar_senha(senha_atual.data):
            raise ValidationError('Senha atual incorreta.')

class FormRecuperarSenha(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    botao_submit_recuperar_senha = SubmitField('Recuperar Senha')
class CadastroEmpresaForm(FlaskForm):
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=14, max=14)])
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    nome_fantasia = StringField('Nome Fantasia', validators=[DataRequired(), Length(min=2, max=100)])
    endereco = StringField('Endereço', validators=[DataRequired(), Length(min=2, max=200)])
    telefones = StringField('Telefones', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Cadastrar Empresa')

class CadastroCaminhaoForm(FlaskForm):
    placa = StringField('Placa', validators=[DataRequired(), Length(min=1, max=10)])
    empresa_id = SelectField('Empresa', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Cadastrar Caminhão')

class CadastroMotoristaForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Cadastrar Motorista')

class CadastroAgendamentoForm(FlaskForm):
    data_chegada = DateField('Data de Chegada', validators=[DataRequired()], format='%Y-%m-%d')
    horario_chegada = TimeField('Horário de Chegada', validators=[DataRequired()], format='%H:%M')
    tempo_estimado = IntegerField('Tempo Estimado (minutos)', validators=[DataRequired()])
    empresa_id = SelectField('Empresa', coerce=int, validators=[DataRequired()])
    caminhao_id = SelectField('Caminhão', coerce=int, validators=[DataRequired()])
    motorista_id = SelectField('Motorista', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Cadastrar Agendamento')

# Formulários para a alteração
class AlterarEmpresaForm(CadastroEmpresaForm):
    submit = SubmitField('Atualizar Empresa')

class AlterarCaminhaoForm(CadastroCaminhaoForm):
    submit = SubmitField('Atualizar Caminhão')

class AlterarMotoristaForm(CadastroMotoristaForm):
    submit = SubmitField('Atualizar Motorista')

class AlterarAgendamentoForm(CadastroAgendamentoForm):
    submit = SubmitField('Atualizar Agendamento')