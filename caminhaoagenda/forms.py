from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from caminhaoagenda.models import Usuario
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistroForm(FlaskForm):
    nome_usuario = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está cadastrado. Escolha outro.')

class EsqueceuSenhaForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired()])
    confirmar_nova_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('nova_senha')])
    submit = SubmitField('Redefinir Senha')

class EditarPerfilNomeEmailForm(FlaskForm):
    novo_nome = StringField('Novo Nome', validators=[InputRequired(), Length(min=2, max=20)])
    novo_email = StringField('Novo Email', validators=[InputRequired(), Email()])


class EditarPerfilSenhaForm(FlaskForm):
    senha_atual = PasswordField('Senha Atual', validators=[InputRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[InputRequired(), Length(min=6)])
    confirmar_nova_senha = PasswordField('Confirmar Nova Senha', validators=[InputRequired(), EqualTo('nova_senha', message='As senhas devem ser iguais.')])

