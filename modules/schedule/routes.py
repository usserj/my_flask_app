# my_flask_app/modules/schedule/routes.py

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required
from datetime import time

# Importaciones relativas del módulo actual
from . import schedule_bp
from .forms import ScheduleForm
from .models import Schedule

# Importaciones globales y de otros módulos
from my_flask_app.extensions import db
from my_flask_app.decorators import role_required

# ==============================================================================
# RUTA PARA GESTIONAR HORARIOS
# ==============================================================================
@schedule_bp.route('/manage', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def manage_schedules():
    """
    Muestra una lista de todos los horarios y maneja la creación de nuevos.
    """
    form = ScheduleForm()
    
    if form.validate_on_submit():
        # Verificar si ya existe un horario idéntico para ese médico y día/hora
        existing_schedule = Schedule.query.filter_by(
            doctor_id=form.doctor_id.data,
            day_of_week=form.day_of_week.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        ).first()

        if existing_schedule:
            flash('Ya existe un horario idéntico para este médico.', 'warning')
        else:
            new_schedule = Schedule(
                doctor_id=form.doctor_id.data,
                day_of_week=form.day_of_week.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                is_active=form.is_active.data
            )
            db.session.add(new_schedule)
            db.session.commit()
            flash('Nuevo horario creado con éxito.', 'success')
        
        return redirect(url_for('schedule.manage_schedules'))

    # Obtenemos todos los horarios y los ordenamos para una mejor visualización
    schedules = Schedule.query.order_by(Schedule.doctor_id, Schedule.day_of_week, Schedule.start_time).all()
    
    # Mapeo de número de día a nombre para mostrar en la plantilla
    day_map = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    
    # Plantilla real del proyecto para gestionar horarios
    return render_template('manage_horarios.html', 
                           schedules=schedules, 
                           form=form, 
                           day_map=day_map,
                           title="Gestionar Horarios")

# ==============================================================================
# RUTA PARA EDITAR UN HORARIO
# ==============================================================================
@schedule_bp.route('/edit/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
@role_required('Administrador')
def edit_schedule(schedule_id):
    """Maneja la edición de un bloque de horario existente."""
    schedule_to_edit = Schedule.query.get_or_404(schedule_id)
    form = ScheduleForm(obj=schedule_to_edit)

    if form.validate_on_submit():
        schedule_to_edit.doctor_id = form.doctor_id.data
        schedule_to_edit.day_of_week = form.day_of_week.data
        schedule_to_edit.start_time = form.start_time.data
        schedule_to_edit.end_time = form.end_time.data
        schedule_to_edit.is_active = form.is_active.data
        db.session.commit()
        flash('Horario actualizado con éxito.', 'success')
        return redirect(url_for('schedule.manage_schedules'))
    
    # Plantilla real del proyecto para editar horarios
    return render_template('edit_horario.html', form=form, title="Editar Horario")

# ==============================================================================
# RUTA PARA "ELIMINAR" (INACTIVAR) UN HORARIO
# ==============================================================================
@schedule_bp.route('/delete/<int:schedule_id>', methods=['POST'])
@login_required
@role_required('Administrador')
def delete_schedule(schedule_id):
    """Inactiva un bloque de horario en lugar de borrarlo permanentemente."""
    schedule_to_delete = Schedule.query.get_or_404(schedule_id)
    schedule_to_delete.is_active = False
    db.session.commit()
    flash('El horario ha sido desactivado.', 'success')
    return redirect(url_for('schedule.manage_schedules'))