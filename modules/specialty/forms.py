# my_flask_app/modules/specialty/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

# Importamos el modelo de este mismo módulo de forma relativa
from .models import Specialty

# ==============================================================================
# FORMULARIO PARA CREAR Y EDITAR ESPECIALIDADES
# ==============================================================================
class SpecialtyForm(FlaskForm):
    """Formulario para gestionar las especialidades médicas."""
    name = StringField('Nombre de la Especialidad', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, max=100)
    ])
    description = TextAreaField('Descripción', validators=[Length(max=500)])
    is_active = SelectField('Estado', choices=[
        (True, 'Activa'),
        (False, 'Inactiva')
    ], coerce=bool) # coerce=bool convierte el 'True'/'False' del form en un booleano real
    submit = SubmitField('Guardar Especialidad')

    def __init__(self, specialty_obj=None, *args, **kwargs):
        """
        Constructor mejorado para manejar la edición.

        Args:
            specialty_obj (Specialty): El objeto que se está editando.
        """
        super(SpecialtyForm, self).__init__(*args, **kwargs)
        self.specialty_obj = specialty_obj

    def validate_name(self, name):
        """Verifica que el nombre de la especialidad no esté repetido."""
        query = Specialty.query.filter_by(name=name.data)
        # Si estamos editando, excluimos la especialidad actual de la búsqueda.
        if self.specialty_obj:
            query = query.filter(Specialty.id != self.specialty_obj.id)
        
        if query.first():
            raise ValidationError('Ya existe una especialidad con este nombre.')

# ==============================================================================
# FORMULARIO PARA ASIGNAR ESPECIALIDADES A DOCTORES
# ==============================================================================
class AssignSpecialtyForm(FlaskForm):
    """Formulario para asignar una o más especialidades a un doctor."""
    doctor_id = SelectField('Seleccionar Médico', coerce=int, validators=[DataRequired()])
    # SelectMultipleField permite seleccionar varias opciones
    specialty_ids = SelectField('Seleccionar Especialidades', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Asignar Especialidades')

    def __init__(self, *args, **kwargs):
        """
        Puebla las opciones de los menús desplegables.
        """
        super(AssignSpecialtyForm, self).__init__(*args, **kwargs)
        # Importamos aquí para evitar importaciones circulares a nivel de módulo
        from my_flask_app.modules.doctor.models import Doctor
        self.doctor_id.choices = [
            (d.id, f"{d.user.first_name} {d.user.last_name}") for d in Doctor.query.join(User).all()
        ]
        self.specialty_ids.choices = [
            (s.id, s.name) for s in Specialty.query.filter_by(is_active=True).all()
        ]