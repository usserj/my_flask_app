# my_flask_app/modules/appointment/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField, StringField
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired, Optional

class AppointmentForm(FlaskForm):
    """Formulario para crear y editar citas médicas."""
    patient_id = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    specialty_id = SelectField('Especialidad', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Médico', coerce=int, validators=[DataRequired()])
    
    appointment_date = DateField('Fecha de la Cita', format='%Y-%m-%d', validators=[DataRequired()])
    appointment_time = TimeField('Hora de la Cita', format='%H:%M', validators=[DataRequired()])
    
    reason = TextAreaField('Motivo de la Cita', validators=[DataRequired()])
    status = SelectField('Estado', choices=[
        ('Programada', 'Programada'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada')
    ])
    submit = SubmitField('Guardar Cita')

    def __init__(self, *args, **kwargs):
        """Puebla los menús desplegables con datos de la BD."""
        super(AppointmentForm, self).__init__(*args, **kwargs)
        from my_flask_app.modules.patient.models import Patient
        from my_flask_app.modules.doctor.models import Doctor
        from my_flask_app.modules.specialty.models import Specialty
        
        self.patient_id.choices = [(p.id, f"{p.user.first_name} {p.user.last_name}") for p in Patient.query.all()]
        self.specialty_id.choices = [(s.id, s.name) for s in Specialty.query.filter_by(is_active=True).all()]
        self.doctor_id.choices = [(d.id, f"{d.user.first_name} {d.user.last_name}") for d in Doctor.query.all()]

class DiagnosisForm(FlaskForm):
    """Formulario para registrar un diagnóstico en una cita."""
    description = TextAreaField('Descripción del Diagnóstico', validators=[DataRequired()])
    prescription = TextAreaField('Receta Médica', validators=[Optional()])
    submit = SubmitField('Guardar Diagnóstico')

class ExamForm(FlaskForm):
    """Formulario para solicitar un examen médico."""
    exam_type = StringField('Tipo de Examen', validators=[DataRequired()])
    description = TextAreaField('Descripción/Indicaciones', validators=[Optional()])
    submit = SubmitField('Solicitar Examen')