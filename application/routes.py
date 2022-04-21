"""Application routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models import Persona, db


@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/guardar_nombre", methods=['POST'])
def guardar_nombre():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nombre_aux = Persona(nombre = nombre)
        db.session.add(nombre_aux)
        db.session.commit()
        print(nombre)
        return 'received'
@app.route("/otros/")
def otros():
    return "<h1> otros </h1>"