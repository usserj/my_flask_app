from flask import Blueprint

office_bp = Blueprint(
    'office', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    static_url_path='/office/static'
)

from . import routes
