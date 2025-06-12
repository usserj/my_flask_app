# my_flask_app/modules/schedule/models.py

from my_flask_app.extensions import db

# ==============================================================================
# MODELO DE HORARIO
# ==============================================================================
class Schedule(db.Model):
    """
    Representa un bloque de tiempo en el que un médico está disponible.
    Ej: Dr. Smith, Lunes, de 09:00 a 12:00.
    """
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    
    # --- Clave Foránea ---
    # Conexión con el modelo Doctor. Cada horario pertenece a un doctor.
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    # --- Campos del Horario ---
    # Usamos un Integer para el día de la semana (0=Lunes, 1=Martes, etc.)
    # Es más eficiente y estándar que usar strings.
    day_of_week = db.Column(db.Integer, nullable=False) # Lunes=0, Martes=1, ... Domingo=6
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # --- Relaciones ---
    # Relación muchos a uno con Doctor. Muchos bloques de horario pueden pertenecer a un doctor.
    # El `back_populates` se conectará con la relación en el modelo Doctor.
    doctor = db.relationship('Doctor', back_populates='schedules')


# --- Añadir la relación inversa en el modelo Doctor ---
# Para que la relación funcione en ambos sentidos (y puedas hacer doctor.schedules),
# debemos añadir el otro lado de la relación.
#
# Abre `my_flask_app/modules/doctor/models.py` y, dentro de la clase `Doctor`,
# añade la siguiente relación:
#
# schedules = db.relationship('Schedule', back_populates='doctor', lazy='dynamic')
#