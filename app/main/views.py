from flask import render_template, url_for, abort, flash, redirect
from flask_login import login_required, current_user

from . import main
from .forms import EditProfileForm, EditProfileAdminForm, SearchCepForm
from .viacep_service import ViaCEP
from .. import db
from ..decorators import admin_required
from ..models import User, Role


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    cep_form = SearchCepForm()
    if cep_form.submit_cep.data and cep_form.validate_on_submit():
        viacep_service = ViaCEP(cep_form.cep.data)
        endereco = viacep_service.buscar_cep()
        current_user.logradouro = endereco.logradouro
        current_user.bairro = endereco.bairro
        current_user.cidade = endereco.cidade
        current_user.uf = endereco.uf
        current_user.ibge = endereco.ibge
        current_user.complemento = endereco.complemento
        current_user.cep = cep_form.cep.data
        current_user.name = cep_form.name.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
    if form.submit.data and form.validate_on_submit():
        current_user.name = cep_form.name.data
        current_user.complemento = form.complemento.data
        current_user.numero_casa = form.numero_casa.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Seu perfil foi atualizado.')
        return redirect(url_for('.user', username=current_user.username))
    cep_form.name.data = current_user.name
    cep_form.cep.data = current_user.cep
    form.logradouro.data = current_user.logradouro
    form.bairro.data = current_user.bairro
    form.cidade.data = current_user.cidade
    form.uf.data = current_user.uf
    form.ibge.data = current_user.ibge
    form.complemento.data = current_user.complemento
    form.numero_casa.data = current_user.numero_casa
    return render_template('edit_profile.html', form=form, cep_form=cep_form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        db.session.add(user)
        db.session.commit()
        flash('O perfil foi atualizado.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    return render_template('edit_profile.html', form=form, user=user)
