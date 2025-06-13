from flask import Flask
from my_flask_app.extensions import db, login_manager, bcrypt


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from my_flask_app.modules.user import user_bp
    from my_flask_app.modules.patient import patient_bp
    from my_flask_app.modules.appointment import appointment_bp
    from my_flask_app.modules.doctor import doctor_bp
    from my_flask_app.modules.schedule import schedule_bp
    from my_flask_app.modules.specialty import specialty_bp

    app.register_blueprint(user_bp, url_prefix='/')
    app.register_blueprint(patient_bp, url_prefix='/paciente')
    app.register_blueprint(appointment_bp, url_prefix='/cita')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(schedule_bp, url_prefix='/horario')
    app.register_blueprint(specialty_bp, url_prefix='/especialidad')

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
