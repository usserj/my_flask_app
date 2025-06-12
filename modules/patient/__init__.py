from flask import Blueprint

patient_bp = Blueprint(
    'patient', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    static_url_path='/patient/static'
)

from . import routes
