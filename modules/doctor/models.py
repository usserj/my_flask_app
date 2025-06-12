# my_flask_app/modules/doctor/models.py

from my_flask_app.extensions import db
from my_flask_app.modules.user.models import User # Importamos el modelo User

# ==============================================================================
# MODELO DE DOCTOR
# ==============================================================================
class Doctor(db.Model):
    """
    Almacena la información ESPECÍFICA de un doctor.
    Hereda la información personal (nombre, etc.) del modelo User.
    """
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    license_number = db.Column(db.String(50), nullable=True)
    hire_date = db.Column(db.Date, nullable=True)

    # --- Relaciones ---
    # Conexión 1-a-1 con el modelo User
    user = db.relationship('User', back_populates='doctor_profile')
    
    # Conexión Muchos-a-Muchos con el modelo Specialty (se definirá en el módulo specialty)
    # Esta relación se completará cuando creemos el modelo Specialty.
    specialties = db.relationship(
        'Specialty',
        secondary='doctor_specialties',
        back_populates='doctors'
    )
# Esta relación permite acceder a todos los horarios de un doctor (ej. my_doctor.schedules.all())
schedules = db.relationship('Schedule', back_populates='doctor', lazy='dynamic')