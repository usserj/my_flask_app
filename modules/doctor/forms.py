# my_flask_app/modules/doctor/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, Optional

from .models import Doctor
from my_flask_app.modules.user.models import User, Catalog

# ==============================================================================
# FORMULARIO PARA CREAR Y EDITAR DOCTORES
# ==============================================================================
class DoctorForm(FlaskForm):
    """Formulario unificado para gestionar la información de un doctor."""
    identification = StringField('Identificación (Cédula)', validators=[DataRequired()])
    first_name = StringField('Nombres', validators=[DataRequired()])
    last_name = StringField('Apellidos', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono')
    city = SelectField('Ciudad de Residencia', choices=[], validators=[DataRequired()])
    license_number = StringField('Número de Licencia', validators=[DataRequired()])
    hire_date = DateField('Fecha de Contratación', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Guardar Doctor')

    def __init__(self, user_obj=None, *args, **kwargs):
        """Constructor mejorado para manejar la edición."""
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.user_obj = user_obj
        self.city.choices = [('', 'Seleccione...')] + [(c.value, c.value) for c in Catalog.query.filter_by(type='ciudad').all()]

    def validate_identification(self, identification):
        query = User.query.filter_by(identification=identification.data)
        if self.user_obj:
            query = query.filter(User.id != self.user_obj.id)
        if query.first():
            raise ValidationError('Esta identificación ya está registrada.')

    def validate_email(self, email):
        query = User.query.filter_by(email=email.data)
        if self.user_obj:
            query = query.filter(User.id != self.user_obj.id)
        if query.first():
            raise ValidationError('Este correo electrónico ya está registrado.')