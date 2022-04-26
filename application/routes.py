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
        admi_aux = Admin(nombre=nombre, email=email)
        db.session.add(admi_aux)
        db.session.commit()
        return 'received'


@app.route("/otros/")
def otros():
    return "<h1> otros </h1>"


@app.route("/crear_nueva_encuesta", methods=['POST'])
def crea_nueva_encuesta():
    if request.method == "POST":
        # output = request.get_json()
        # print(output)
        num = request.form.get("ola")
        print(num)
        return "value recieved"
    return render_template("admin/survey.html")

    # if db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first() == None:
    #     return redirect("/survey/1/preguntas")
    # else:
    #     id_ultima_encuesta = db.session.query(Encuesta).order_by(
    #         Encuesta.id_encuesta.desc()).first().id_encuesta
    #     id_nueva = id_ultima_encuesta + 1
    #     return redirect("/survey/"+str(id_nueva)+"/preguntas")


@ app.route("/survey/, methods=['POST']")
@ app.route("/survey/<int:id>/")
@ app.route("/survey/<int:id>/<string:section>")
def Survey(id=0, section="preguntas"):
    # Tarea 1: Si se ingresa con la ruta /survey/ lo que hay que hacer es consultar el ultimo id creado de encuesta (Traerlo y almacenarlo en una var).
    # Tarea 2: Si se ingresa con la ruta /survey/id se debe preguntar a la base de datos si el id existe. Si existe se trae la info de la encuesta.
    dataSurvey = {
        "id": "",
        "title": "",
        "description": "",
        "questions": [
            {
                "id": "1",
                "statement": "holaloquito",
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
