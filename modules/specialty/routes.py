# my_flask_app/modules/specialty/routes.py

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required

# Importaciones relativas del módulo actual
from . import specialty_bp
from .forms import SpecialtyForm, AssignSpecialtyForm
from .models import Specialty

# Importaciones de otros módulos y globales
from my_flask_app.modules.doctor.models import Doctor
from my_flask_app.extensions import db
from my_flask_app.decorators import role_required

# ==============================================================================
# RUTA PARA GESTIONAR ESPECIALIDADES
# ==============================================================================
@specialty_bp.route('/manage', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def manage_specialties():
    """Muestra y permite crear/editar especialidades."""
    form = SpecialtyForm()
    
    if form.validate_on_submit():
        new_specialty = Specialty(
            name=form.name.data,
            description=form.description.data,
            is_active=form.is_active.data
        )
        db.session.add(new_specialty)
        db.session.commit()
        flash(f"Especialidad '{form.name.data}' creada con éxito.", 'success')
        return redirect(url_for('specialty.manage_specialties'))

    specialties = Specialty.query.all()
    # Plantilla real del proyecto para gestionar especialidades
    return render_template('manage_specialties.html', specialties=specialties, form=form, title="Gestionar Especialidades")

# ==============================================================================
# RUTA PARA EDITAR UNA ESPECIALIDAD
# ==============================================================================
@specialty_bp.route('/edit/<int:specialty_id>', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def edit_specialty(specialty_id):
    """Maneja la edición de una especialidad existente."""
    specialty = Specialty.query.get_or_404(specialty_id)
    # Pasamos el objeto al formulario para que el validador de unicidad funcione
    form = SpecialtyForm(specialty_obj=specialty)

    if form.validate_on_submit():
        specialty.name = form.name.data
        specialty.description = form.description.data
        specialty.is_active = form.is_active.data
        db.session.commit()
        flash('Especialidad actualizada con éxito.', 'success')
        return redirect(url_for('specialty.manage_specialties'))

    # Poblar el formulario con los datos existentes en la solicitud GET
    elif request.method == 'GET':
        form.name.data = specialty.name
        form.description.data = specialty.description
        form.is_active.data = specialty.is_active

    # Plantilla real del proyecto para editar una especialidad
    return render_template('edit_specialty.html', form=form, title="Editar Especialidad")

# ==============================================================================
# RUTA PARA ASIGNAR ESPECIALIDADES A UN DOCTOR
# ==============================================================================
@specialty_bp.route('/assign', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def assign_specialty():
    """Maneja la asignación de una o más especialidades a un médico."""
    form = AssignSpecialtyForm()
    
    if form.validate_on_submit():
        doctor = Doctor.query.get(form.doctor_id.data)
        if not doctor:
            flash('Médico no encontrado.', 'danger')
            return redirect(url_for('specialty.assign_specialty'))
            
        # Limpiamos las especialidades anteriores para evitar duplicados
        doctor.specialties.clear()
        
        # Asignamos las nuevas especialidades seleccionadas
        selected_specialties = Specialty.query.filter(Specialty.id.in_(form.specialty_ids.data)).all()
        for spec in selected_specialties:
            doctor.specialties.append(spec)
        
        db.session.commit()
        flash(f'Especialidades actualizadas para el Dr. {doctor.user.last_name}.', 'success')
        return redirect(url_for('specialty.assign_specialty'))
        
    # Plantilla real del proyecto para asignar especialidades
    return render_template('assign_specialties.html', form=form, title="Asignar Especialidades")