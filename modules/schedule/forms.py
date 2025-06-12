# my_flask_app/modules/schedule/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.fields import TimeField # Asegurarse de importar TimeField
from wtforms.validators import DataRequired

# ==============================================================================
# FORMULARIO PARA CREAR Y EDITAR HORARIOS
# ==============================================================================
class ScheduleForm(FlaskForm):
    """Formulario para gestionar los bloques de horario de un médico."""
    
    doctor_id = SelectField('Seleccionar Médico', coerce=int, validators=[
        DataRequired(message="Debe seleccionar un médico.")
    ])
    
    # Usamos enteros para los días de la semana (Lunes=0, Martes=1, etc.)
    # Esto coincide con el modelo y es una mejor práctica.
    day_of_week = SelectField('Día de la Semana', coerce=int, choices=[
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo')
    ], validators=[DataRequired()])
    
    start_time = TimeField('Hora de Inicio', validators=[DataRequired()])
    end_time = TimeField('Hora de Fin', validators=[DataRequired()])
    
    is_active = SelectField('Estado', coerce=bool, choices=[
        (True, 'Activo'),
        (False, 'Inactivo')
    ])
    
    submit = SubmitField('Guardar Horario')

    def __init__(self, *args, **kwargs):
        """
        Puebla las opciones del menú desplegable de doctores.
        """
        super(ScheduleForm, self).__init__(*args, **kwargs)
        # Importamos aquí para evitar importaciones circulares
        from my_flask_app.modules.doctor.models import Doctor
        from my_flask_app.modules.user.models import User
        # Creamos una lista de tuplas (id, "Nombre Apellido") para las opciones
        self.doctor_id.choices = [
            (d.id, f"{d.user.first_name} {d.user.last_name}") 
            for d in Doctor.query.join(User).all()
        ]