from my_flask_app.extensions import db


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=False)

    appointment_time = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Programada')

    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', backref='appointments', lazy='dynamic')
    specialty = db.relationship('Specialty', backref='appointments', lazy='dynamic')

    diagnoses = db.relationship('Diagnosis', back_populates='appointment', cascade='all, delete-orphan')
    exams = db.relationship('Exam', back_populates='appointment', cascade='all, delete-orphan')


class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text)

    appointment = db.relationship('Appointment', back_populates='diagnoses')


class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    exam_type = db.Column(db.String(128))
    result = db.Column(db.Text)

    appointment = db.relationship('Appointment', back_populates='exams')
