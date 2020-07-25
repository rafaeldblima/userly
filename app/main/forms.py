from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, Email

from app.models import User, Role


class NameForm(FlaskForm):
    name = StringField('Qual seu nome?', validators=[DataRequired()])
    submit = SubmitField('Salvar')


class SearchCepForm(FlaskForm):
    name = StringField('Nome', validators=[Length(0, 255)])
    cep = StringField('CEP', validators=[
        DataRequired(),
        Length(1,10),
        Regexp('^\d{5}-\d{3}$', 0,
               '00000-000.')
    ])
    submit_cep = SubmitField('Buscar cep')


class EditProfileForm(FlaskForm):
    logradouro = StringField('Logradouro', validators=[Length(0, 255)], render_kw={'readonly': True})
    bairro = StringField('Bairro', validators=[Length(0, 255)], render_kw={'readonly': True})
    cidade = StringField('Cidade', validators=[Length(0, 255)], render_kw={'readonly': True})
    uf = StringField('UF', validators=[Length(0, 255)], render_kw={'readonly': True})
    ibge = StringField('Ibge', validators=[Length(0, 255)], render_kw={'readonly': True})
    complemento = StringField('Complemento', validators=[Length(0, 255)])
    numero_casa = StringField('Número da casa', validators=[Length(0, 10)])
    submit = SubmitField('Salvar')


class EditProfileAdminForm(FlaskForm):
    email = StringField(
        'E-mail', validators=[DataRequired(), Length(1, 64), Email()]
    )
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
    confirmed = BooleanField('Confirmado')
    role = SelectField('Função', coerce=int)
    name = StringField('Nome', validators=[Length(0, 64)])
    cep = StringField('CEP', validators=[Length(0, 9)])
    submit = SubmitField('Salvar')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('E-mail já registrado.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username já está em uso.')
