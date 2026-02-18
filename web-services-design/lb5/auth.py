from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user


def check_rights(check_func):
    """Decorator factory. check_func(*args, **kwargs) must return True if access is allowed."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not check_func(*args, **kwargs):
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ── Permission check functions ────────────────────────────────────────────────

def is_admin(*args, **kwargs):
    return current_user.is_authenticated and current_user.is_admin


def can_view_user(user_id=None, **kwargs):
    if not current_user.is_authenticated:
        return False
    return current_user.is_admin or current_user.id == user_id


def can_edit_user(user_id=None, **kwargs):
    if not current_user.is_authenticated:
        return False
    return current_user.is_admin or current_user.id == user_id


def can_view_logs(*args, **kwargs):
    """Both admin and regular user may access the log (filtered differently)."""
    return current_user.is_authenticated
