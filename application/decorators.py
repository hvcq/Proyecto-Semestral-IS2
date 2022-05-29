from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if current_user.rol != "admin":
            abort(401)
        return f(*args, **kws)
    return decorated_function

def registrado_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if current_user.rol != "registrado":
            abort(401)
        return f(*args, **kws)
    return decorated_function

def encuestado_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if current_user.rol != "encuestado":
            abort(401)
        return f(*args, **kws)
    return decorated_function