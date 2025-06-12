from flask import Blueprint

appointment_bp = Blueprint(
    'appointment', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    static_url_path='/appointment/static'
)

from . import routes
