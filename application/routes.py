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


@app.route("/survey/")
@app.route("/survey/<int:id>/<string:section>")
# Arreglar el valor por default de la seccion a mostrar si solo se ingresa a /createSurvey/
def createSurvey(id, section="preguntas"):
    # Aqui tenemos que preguntar a la base de datos cual es el ultimo id creado
    # luego asignamos el id nuevo como el ultimo creado + 1.
    # Ademas en este apartado se deben traer los datos de la encuesta en el caso que pase por parametro

    # Se presenta un ejemplo de como podría llegar la info.
    dataSurvey = {
        "id": "",
        "title": "Mi primera encuesta",
        "description": "Esta es mi primera encuesta ola",
        "questions": [
            {
                "statement": "holaloquito",
                "type": "alternativa",
                "alternatives": ["Opcion1", "Opcion2", "Opcion3"]
            },
            {
                "statement": "¿Cuantos años tienes?",
                "type": "desarrollo",
                "alternatives": []
            }
        ]
    }
    return render_template("admin/survey.html", data={
        "options": ["Preguntas", "Respuestas", "Configuración"],
        "selected": section,
        "id": id,
        "dataSurvey": dataSurvey
    }
    )
