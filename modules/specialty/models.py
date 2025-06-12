# my_flask_app/modules/specialty/models.py

from my_flask_app.extensions import db

# ==============================================================================
# TABLA DE ASOCIACIÓN (Doctor <-> Especialidad)
# ==============================================================================
# Esta tabla intermedia permite que un doctor tenga múltiples especialidades y
# que una especialidad pueda ser asignada a múltiples doctores.
doctor_specialties = db.Table('doctor_specialties',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctors.id'), primary_key=True),
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialties.id'), primary_key=True)
)

# ==============================================================================
# MODELO DE ESPECIALIDAD
# ==============================================================================
class Specialty(db.Model):
    """
    Representa una especialidad médica (Ej: Cardiología, Pediatría).
    """
    __tablename__ = 'specialties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # --- Relaciones ---
    # Relación muchos a muchos con Doctor.
    # El `back_populates` se conectará con la relación en el modelo Doctor.
    doctors = db.relationship(
        'Doctor', 
        secondary=doctor_specialties, 
        back_populates='specialties'
    )

# --- Añadir la relación inversa en el modelo Doctor ---
# Para que la relación funcione en ambos sentidos, debemos añadir el otro lado.
# Abre `my_flask_app/modules/doctor/models.py` y, dentro de la clase `Doctor`,
# añade la siguiente relación:
#
# specialties = db.relationship(
#     'Specialty',
#     secondary='doctor_specialties', # Nombre de la tabla de asociación que creamos aquí
#     back_populates='doctors'
# )
#