# my_flask_app/modules/appointment/routes.py

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from datetime import datetime

from . import appointment_bp
from .forms import AppointmentForm, DiagnosisForm
from .models import Appointment, Diagnosis
from my_flask_app.extensions import db
from my_flask_app.decorators import role_required

@appointment_bp.route('/manage')
@login_required
@role_required('Administrador')
def manage_appointments():
    """Muestra una lista de todas las citas del sistema."""
    appointments = Appointment.query.order_by(Appointment.appointment_time.desc()).all()
    return render_template('manage_citas.html', appointments=appointments, title="Gestionar Citas")

@appointment_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_appointment():
    """Permite crear una nueva cita (accesible por admin o paciente)."""
    form = AppointmentForm()
    if form.validate_on_submit():
        # Combinar fecha y hora en un solo objeto datetime
        combined_datetime = datetime.combine(form.appointment_date.data, form.appointment_time.data)
        
        new_appointment = Appointment(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            specialty_id=form.specialty_id.data,
            appointment_time=combined_datetime,
            reason=form.reason.data,
            status=form.status.data,
            created_by_user_id=current_user.id
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Cita creada con éxito.', 'success')
        
        # Redirigir según el rol
        if 'Administrador' in [role.name for role in current_user.roles]:
            return redirect(url_for('appointment.manage_appointments'))
        else:
            # Asumimos que hay una ruta para que el paciente vea sus citas
            return redirect(url_for('patient.my_appointments')) 
            
    # La plantilla a renderizar puede variar según el rol
    template = 'create_cita.html' # Plantilla para admin
    if 'Paciente' in [role.name for role in current_user.roles]:
        template = 'paciente_crear_cita.html' # Plantilla para paciente
        
    return render_template(template, form=form, title="Crear Nueva Cita")

@appointment_bp.route('/<int:appointment_id>/view', methods=['GET', 'POST'])
@login_required
def view_appointment(appointment_id):
    """Muestra los detalles de una cita y permite añadir diagnósticos."""
    appointment = Appointment.query.get_or_404(appointment_id)
    diag_form = DiagnosisForm()

    if diag_form.validate_on_submit():
        if 'Medico' not in [role.name for role in current_user.roles]:
            flash('Solo los médicos pueden añadir diagnósticos.', 'danger')
            return redirect(url_for('appointment.view_appointment', appointment_id=appointment.id))

        new_diagnosis = Diagnosis(
            appointment_id=appointment.id,
            description=diag_form.description.data,
            prescription=diag_form.prescription.data
        )
        db.session.add(new_diagnosis)
        appointment.status = 'Completada' # Cambiar estado de la cita
        db.session.commit()
        flash('Diagnóstico añadido y cita marcada como completada.', 'success')
        return redirect(url_for('appointment.view_appointment', appointment_id=appointment.id))
    
    # La plantilla que muestra los detalles de una cita (podría ser 'ver_cita.html')
    # Usaremos 'Medico_registrar_diagnostico.html' como placeholder
    return render_template('Medico_registrar_diagnostico.html', 
                           appointment=appointment, 
                           form=diag_form, 
                           title="Detalle de Cita")