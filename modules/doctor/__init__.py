from flask import Blueprint

doctor_bp = Blueprint(
    'doctor', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    static_url_path='/doctor/static'
)

from . import routes
