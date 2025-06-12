# my_flask_app/modules/patient/routes.py

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required

# Importaciones relativas del módulo actual
from . import patient_bp
from .forms import PatientForm
from .models import Patient

# Importaciones de otros módulos y globales
from my_flask_app.modules.user.models import User, Role
from my_flask_app.extensions import db, bcrypt
from my_flask_app.decorators import role_required

# ==============================================================================
# RUTA PARA GESTIONAR PACIENTES
# ==============================================================================
@patient_bp.route('/manage')
@login_required
@role_required('Administrador') # Solo los administradores pueden gestionar pacientes
def manage_patients():
    """Muestra una lista de todos los pacientes del sistema."""
    # Obtenemos todos los usuarios que tienen un perfil de paciente asociado.
    # Esta consulta es eficiente y escalable.
    patients = User.query.join(Patient).all()
    return render_template('manage_patients.html', patients=patients, title="Gestionar Pacientes")

# ==============================================================================
# RUTA PARA CREAR UN NUEVO PACIENTE
# ==============================================================================
@patient_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def create_patient():
    """Maneja la creación de un nuevo paciente y su usuario asociado."""
    form = PatientForm()
    if form.validate_on_submit():
        # Crear primero el Usuario asociado con una contraseña por defecto
        hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
        new_user = User(
            username=form.email.data, # Usar email como username inicial
            email=form.email.data,
            password_hash=hashed_password,
            identification=form.identification.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data,
            # Se necesitaría añadir birth_date y gender al formulario si son obligatorios
        )
        
        # Asignar el rol de 'Paciente'
        patient_role = Role.query.filter_by(name='Paciente').first()
        if patient_role:
            new_user.roles.append(patient_role)

        db.session.add(new_user)
        db.session.flush() # flush() para obtener el new_user.id antes del commit

        # Crear el perfil de Paciente y asociarlo al usuario
        new_patient_profile = Patient(
            user_id=new_user.id,
            blood_type=form.blood_type.data
        )
        db.session.add(new_patient_profile)
        db.session.commit()

        flash(f'Paciente {new_user.first_name} {new_user.last_name} creado con éxito.', 'success')
        return redirect(url_for('patient.manage_patients'))

    return render_template('create_patient.html', form=form, title="Añadir Paciente")

# ==============================================================================
# RUTA PARA EDITAR UN PACIENTE EXISTENTE
# ==============================================================================
@patient_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def edit_patient(user_id):
    """Maneja la edición de la información de un paciente."""
    user_to_edit = User.query.get_or_404(user_id)
    patient_profile = user_to_edit.patient_profile # Accedemos al perfil de paciente

    # Pasamos el perfil del paciente como 'obj' para que el validador funcione
    form = PatientForm(obj=patient_profile)

    if form.validate_on_submit():
        # Actualizar los datos del Usuario
        user_to_edit.identification = form.identification.data
        user_to_edit.first_name = form.first_name.data
        user_to_edit.last_name = form.last_name.data
        user_to_edit.email = form.email.data
        user_to_edit.phone = form.phone.data
        user_to_edit.address = form.address.data
        user_to_edit.city = form.city.data
        
        # Actualizar los datos del Paciente
        if patient_profile:
            patient_profile.blood_type = form.blood_type.data

        db.session.commit()
        flash('Paciente actualizado con éxito.', 'success')
        return redirect(url_for('patient.manage_patients'))

    # Poblar el formulario con los datos existentes al cargar la página (método GET)
    form.identification.data = user_to_edit.identification
    form.first_name.data = user_to_edit.first_name
    form.last_name.data = user_to_edit.last_name
    form.email.data = user_to_edit.email
    form.phone.data = user_to_edit.phone
    form.address.data = user_to_edit.address
    form.city.data = user_to_edit.city
    if patient_profile:
        form.blood_type.data = patient_profile.blood_type

    return render_template('edit_patient.html', form=form, title="Editar Paciente")