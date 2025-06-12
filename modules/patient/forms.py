# my_flask_app/modules/patient/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

# Importamos los modelos necesarios de forma relativa
from .models import Patient
from my_flask_app.modules.user.models import User, Catalog

# ==============================================================================
# FORMULARIO PARA CREAR Y EDITAR PACIENTES
# ==============================================================================
class PatientForm(FlaskForm):
    """
    Este formulario gestiona la información específica del paciente.
    La información general (nombre, cédula, etc.) se tomará del
    formulario de usuario para mantener la consistencia.
    """
    # --- Campos Específicos del Paciente ---
    blood_type = SelectField('Grupo Sanguíneo', choices=[], validators=[DataRequired()])
    
    # --- Campos del Usuario Asociado (para edición y creación) ---
    # Usaremos los mismos nombres de campo que en el UserRegistrationForm para facilitar el mapeo.
    identification = StringField('Identificación (Cédula)', validators=[DataRequired()])
    first_name = StringField('Nombres', validators=[DataRequired()])
    last_name = StringField('Apellidos', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono')
    address = StringField('Dirección')
    city = SelectField('Ciudad de Residencia', choices=[], validators=[DataRequired()])
    
    submit = SubmitField('Guardar Paciente')

    def __init__(self, *args, **kwargs):
        """Carga las opciones dinámicas de los catálogos."""
        super(PatientForm, self).__init__(*args, **kwargs)
        # Cargar tipos de sangre desde el catálogo
        self.blood_type.choices = [('', 'Seleccione...')] + [(c.value, c.value) for c in Catalog.query.filter_by(type='grupo_sanguineo').all()]
        # Cargar ciudades desde el catálogo
        self.city.choices = [('', 'Seleccione...')] + [(c.value, c.value) for c in Catalog.query.filter_by(type='ciudad').all()]

    def validate_identification(self, identification):
        """Verifica que la identificación no pertenezca a otro usuario."""
        # Esta lógica se aplica principalmente al crear un nuevo paciente.
        # Al editar, necesitaremos excluir al usuario actual de la validación.
        user = User.query.filter_by(identification=identification.data).first()
        # 'self.obj' es una forma de acceder al objeto que se está editando.
        if user and (not self.obj or self.obj.user_id != user.id):
            raise ValidationError('Esta identificación ya está registrada.')

    def validate_email(self, email):
        """Verifica que el correo no pertenezca a otro usuario."""
        user = User.query.filter_by(email=email.data).first()
        if user and (not self.obj or self.obj.user_id != user.id):
            raise ValidationError('Este correo electrónico ya está registrado.')