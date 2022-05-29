"""Aqui se da inicio a la aplicacion"""
from flask import Flask
# login_required se encarga de que las rutas sean accesibles por un usuario loggeado
from flask_sqlalchemy import SQLAlchemy
# from ddtrace import patch_all  <-- ddtrace no lo usaremos por ahora
from flask_wtf.csrf import CSRFProtect
# CSRFProtect permite uso de token para proteger formularios

db = SQLAlchemy()
# patch_all() <-- esto da bug

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    csrf = CSRFProtect()
    app.config.from_object("config.Config")
    
    db.init_app(app)
    csrf.init_app(app)
    
    with app.app_context():
        from . import routes  # Import routes
        # Reinicia las tabla cada vez que se inicia ejecuta
        # db.drop_all()
        # db.create_all()
        return app
