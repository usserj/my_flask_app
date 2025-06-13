from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')


class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    identification = StringField('Identificación')
    first_name = StringField('Nombres')
    last_name = StringField('Apellidos')
    phone = StringField('Teléfono')
    address = StringField('Dirección')
    city = StringField('Ciudad')
    submit = SubmitField('Registrar')
