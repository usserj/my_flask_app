# my_flask_app/modules/appointment/models.py

from my_flask_app.extensions import db

# ==============================================================================
# MODELO DE CITA (APPOINTMENT)
# ==============================================================================
class Appointment(db.Model):
    """
    Representa una cita médica. Es el modelo central que conecta a
    pacientes, doctores y especialidades en un evento específico.
    """
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    
    # --- Claves Foráneas ---
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=False)
    
    # --- Campos de la Cita ---
    appointment_time = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    reason = db.Column(db.Text, nullable=True) # Motivo de la cita
    status = db.Column(db.String(50), nullable=False, default='Programada') # Ej: Programada, Completada, Cancelada
    
    # --- Metadatos ---
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    # --- Relaciones ---
    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', backref='appointments', lazy='dynamic')
    specialty = db.relationship('Specialty', backref='appointments', lazy='dynamic')
    
    # Relación uno a muchos con Diagnóstico
    diagnoses = db.relationship('Diagnosis', back_populates='appointment', cascade="all, delete-orphan")
    # Relación uno a muchos con Examen
    exams = db.relationship('Exam', back_populates='appointment', cascade="all, delete-orphan")

# ==============================================================================
# MODELO DE DIAGNÓSTICO
# ==============================================================================
class Diagnosis