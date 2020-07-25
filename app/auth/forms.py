from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Mantenha me logado')
    submit = SubmitField('Log In')


class CepForm(FlaskForm):
    cep = StringField('CEP', validators=[
        DataRequired(),
        Length(1,10),
        Regexp('^\d{5}-\d{3}$', 0,
               '00000-000.')
    ])
    submit_cep = SubmitField('Buscar cep')


class RegistrationForm(FlaskForm):
    logradouro = StringField('Logradouro', validators=[Length(0, 255)], render_kw={'readonly': True})
    bairro = StringField('Bairro', validators=[Length(0, 255)], render_kw={'readonly': True})
    cidade = StringField('Cidade', validators=[Length(0, 255)], render_kw={'readonly': True})
    uf = StringField('UF', validators=[Length(0, 255)], render_kw={'readonly': True})
    ibge = StringField('Ibge', validators=[Length(0, 255)], render_kw={'readonly': True})
    complemento = StringField('Complemento', validators=[Length(0, 255)])
    numero_casa = StringField('Número da casa', validators=[Length(0, 10)])
    email = StringField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                   'Usernames devem ser somente letras, números,'
                   ' pontos ou underlines.')
        ]
    )
    password = PasswordField(
        'Senha',
        validators=[
            DataRequired(), EqualTo('password2', message='Senhas precisam ser iguais.')
        ]
    )
    password2 = PasswordField('Confirmar senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email já registrado.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username já está em uso.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Antiga senha', validators=[DataRequired()])
    password = PasswordField(
        'Nova senha', validators=[
            DataRequired(), EqualTo('password2', message='Senhas precisam ser iguais.')
        ]
    )
    password2 = PasswordField('Cofirme a nova senha',
                              validators=[DataRequired()])
    submit = SubmitField('Atualize a senha')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Resetar senha')


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        'Nova Senha',
        validators=[
            DataRequired(), EqualTo('password2', message='Senhas precisam ser igual')
        ]
    )
    password2 = PasswordField('Confirme a senha', validators=[DataRequired()])
    submit = SubmitField('Resetar senha')


class ChangeEmailForm(FlaskForm):
    email = StringField('Novo e-mail', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Atualizer e-mail')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('E-mail já registrado.')
