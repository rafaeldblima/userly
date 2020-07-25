from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, \
    ChangeEmailForm, CepForm
from .. import db
from ..email import send_email
from ..main.viacep_service import ViaCEP
from ..models import User


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Você confirmou sua conta. Obrigado!')
    else:
        flash('O link de confirmação é inválido ou expirou.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirme sua conta',
               'auth/email/confirm', user=current_user, token=token)
    flash('Um novo e-mail de confirmação foi enviado para você por e-mail.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data, force=True)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('E-mail ou password inválidos.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi deslogado.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    cep_form = CepForm()
    if cep_form.submit_cep.data and cep_form.validate_on_submit():
        viacep_service = ViaCEP(cep_form.cep.data)
        endereco = viacep_service.buscar_cep()
        form.logradouro.data = endereco.logradouro
        form.bairro.data = endereco.bairro
        form.cidade.data = endereco.cidade
        form.uf.data = endereco.uf
        form.ibge.data = endereco.ibge
        form.complemento.data = endereco.complemento
    if form.submit.data and form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            username=form.username.data,
            password=form.password.data,
            cep=cep_form.cep.data,
            logradouro=form.logradouro.data,
            bairro=form.bairro.data,
            cidade=form.cidade.data,
            uf=form.uf.data,
            ibge=form.ibge.data,
            complemento=form.complemento.data,
            numero_casa=form.numero_casa.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirme sua conta',
                   'auth/email/confirm', user=user, token=token)
        flash('Um e-mail de confirmação foi enviado para você por e-mail.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, cep_form=cep_form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Sua senha foi atualizada.')
            return redirect(url_for('main.index'))
        else:
            flash('Senha inválida.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset sua senha',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('Um e-mail com instruções para resetar sua senha foi enviado '
              'para você.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Sua senha foi atualizada.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirme seu endereço de e-mail',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('Um e-mail com instruções para confirmar seu novo endereço '
                  'de e-mail foi enviado para você.')
            return redirect(url_for('main.index'))
        else:
            flash('E-mail ou senha inválidos.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Seu endereço de e-mail foi atualizado.')
    else:
        flash('Request inválida.')
    return redirect(url_for('main.index'))
