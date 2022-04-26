"""Aqui se da inicio a la aplicacion"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from ddtrace import patch_all  <-- ddtrace no lo usaremos por ahora


db = SQLAlchemy()
# patch_all() <-- esto da bug


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app) # Esto no se oculta

    with app.app_context():
        from . import routes  # Import routes
        # Reinicia las tabla cada vez que se inicia ejecuta
        # db.drop_all()
        # db.create_all()
        return app
