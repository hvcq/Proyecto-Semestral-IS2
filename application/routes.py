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
        nombre_aux = Persona(nombre=nombre)
        db.session.add(nombre_aux)
        db.session.commit()
        print(nombre)
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
