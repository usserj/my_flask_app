# my_flask_app/modules/doctor/routes.py

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required

from . import doctor_bp
from .forms import DoctorForm
from .models import Doctor
from my_flask_app.modules.user.models import User, Role
from my_flask_app.extensions import db, bcrypt
from my_flask_app.decorators import role_required

@doctor_bp.route('/manage')
@login_required
@role_required('Administrador')
def manage_doctors():
    doctors_users = User.query.join(Doctor).all()
    return render_template('manage_doctors.html', doctors=doctors_users, title="Gestionar Médicos")

@doctor_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def create_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
        new_user = User(
            username=form.email.data,
            email=form.email.data,
            password_hash=hashed_password,
            identification=form.identification.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            city=form.city.data,
            birth_date="1990-01-01"
        )
        doctor_role = Role.query.filter_by(name='Medico').first()
        if doctor_role:
            new_user.roles.append(doctor_role)
        db.session.add(new_user)
        db.session.flush()
        new_doctor_profile = Doctor(
            user_id=new_user.id,
            license_number=form.license_number.data,
            hire_date=form.hire_date.data
        )
        db.session.add(new_doctor_profile)
        db.session.commit()
        flash(f'Doctor {new_user.first_name} {new_user.last_name} creado.', 'success')
        return redirect(url_for('doctor.manage_doctors'))
    return render_template('create_doctor.html', form=form, title="Añadir Médico")

@doctor_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def edit_doctor(user_id):
    user_to_edit = User.query.get_or_404(user_id)
    doctor_profile = user_to_edit.doctor_profile
    form = DoctorForm(user_obj=user_to_edit)

    if form.validate_on_submit():
        user_to_edit.identification = form.identification.data
        user_to_edit.first_name = form.first_name.data
        user_to_edit.last_name = form.last_name.data
        user_to_edit.email = form.email.data
        user_to_edit.phone = form.phone.data
        user_to_edit.city = form.city.data
        if doctor_profile:
            doctor_profile.license_number = form.license_number.data
            doctor_profile.hire_date = form.hire_date.data
        db.session.commit()
        flash('Información del Doctor actualizada.', 'success')
        return redirect(url_for('doctor.manage_doctors'))

    elif request.method == 'GET':
        form.identification.data = user_to_edit.identification
        form.first_name.data = user_to_edit.first_name
        form.last_name.data = user_to_edit.last_name
        form.email.data = user_to_edit.email
        form.phone.data = user_to_edit.phone
        form.city.data = user_to_edit.city
        if doctor_profile:
            form.license_number.data = doctor_profile.license_number
            form.hire_date.data = doctor_profile.hire_date

    return render_template('edit_doctor.html', form=form, title="Editar Médico", user=user_to_edit)