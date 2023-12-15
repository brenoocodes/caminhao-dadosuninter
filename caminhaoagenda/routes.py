from flask import render_template, url_for, flash, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from caminhaoagenda import app, database, bcrypt
from caminhaoagenda.models import Usuario
from caminhaoagenda.forms import LoginForm, RegistroForm, EsqueceuSenhaForm, EditarPerfilNomeEmailForm, EditarPerfilSenhaForm


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('meu_perfil'))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            return redirect(url_for('meu_perfil'))
        else:
            flash('Credenciais inválidas. Verifique seu email e senha.', 'danger')

    return render_template('login.html', form=form)

@app.route("/meu_perfil", methods=['GET', 'POST'])
@login_required
def meu_perfil():
    form_nome_email = EditarPerfilNomeEmailForm()
    form_senha = EditarPerfilSenhaForm()

    if form_nome_email.validate_on_submit():
        usuario = Usuario.query.get(current_user.id)
        usuario.nome_usuario = form_nome_email.novo_nome.data
        usuario.email = form_nome_email.novo_email.data

        try:
            database.session.commit()
            flash('Perfil atualizado com sucesso.', 'success')
            return redirect(url_for('meu_perfil'))
        except Exception as e:
            database.session.rollback()
            flash(f'Erro ao atualizar perfil: {str(e)}', 'danger')

    if form_senha.validate_on_submit():
        usuario = Usuario.query.get(current_user.id)

        if bcrypt.check_password_hash(usuario.senha, form_senha.senha_atual.data):
            nova_senha_hashed = bcrypt.generate_password_hash(form_senha.nova_senha.data).decode('utf-8')
            usuario.senha = nova_senha_hashed

            try:
                database.session.commit()
                flash('Senha atualizada com sucesso.', 'success')
                return redirect(url_for('meu_perfil'))
            except Exception as e:
                database.session.rollback()
                flash(f'Erro ao atualizar senha: {str(e)}', 'danger')
        else:
            flash('Senha atual incorreta. Tente novamente.', 'danger')

    return render_template('meu_perfil.html', form_nome_email=form_nome_email, form_senha=form_senha)

@app.route("/criar_conta", methods=['GET', 'POST'])
def criar_conta():
    if current_user.is_authenticated:
        return redirect(url_for('meu_perfil'))

    form = RegistroForm()
    if form.validate_on_submit():
        senha_hashed = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(nome_usuario=form.nome_usuario.data, email=form.email.data, senha=senha_hashed)
        database.session.add(usuario)
        database.session.commit()
        flash('Sua conta foi criada! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))

    return render_template('criar_conta.html', form=form)

@app.route("/esqueceu_senha", methods=['GET', 'POST'])
def esqueceu_senha():
    if current_user.is_authenticated:
        return redirect(url_for('meu_perfil'))

    form = EsqueceuSenhaForm()
    if form.validate_on_submit():
        # Lógica para redefinir a senha vai aqui (ainda não implementada nesta versão básica)
        flash('Um email com instruções para redefinir sua senha foi enviado.', 'info')
        return redirect(url_for('login'))

    return render_template('esqueceu_senha.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

