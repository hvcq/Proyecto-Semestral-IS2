"""Rutas de la aplicacion"""
from datetime import datetime as dt

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models import Admin, db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/guardar_admin", methods=['POST'])
def guardar_admin():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        admi_aux = Admin(nombre = nombre,email = email)
        db.session.add(admi_aux)
        db.session.commit()
        return 'received'

@app.route("/otros/")
def otros():
    return "<h1> otros </h1>"


@app.route("/createSurvey/")
@app.route("/createSurvey/<string:section>")
# Arreglar el valor por default de la seccion a mostrar si solo se ingresa a /createSurvey/
def createSurvey(section="preguntas"):
    return render_template("admin/create_survey.html", navOptions={
        "options": ["Preguntas", "Respuestas", "Configuración"],
        "selected": section
    }
    )
