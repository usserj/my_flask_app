from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash


def role_required(role_name):
    """Simple decorator to check if the current user has a given role."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('user.login'))
            if not any(role.name == role_name for role in current_user.roles):
                flash('No tienes permiso para acceder a esta página.', 'danger')
                return redirect(url_for('user.login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator
