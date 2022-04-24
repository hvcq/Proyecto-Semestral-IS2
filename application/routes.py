"""Rutas de la aplicacion"""
from datetime import datetime,date

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models import Admin, Encuesta, db


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

@app.route("/crear_nueva_encuesta", methods=['GET'])
def crea_nueva_encuesta():
    if db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first() == None:
        return redirect("/survey/1/preguntas")
    else:
        id_ultima_encuesta = db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first().id_encuesta
        id_nueva = id_ultima_encuesta + 1
        return redirect("/survey/"+str(id_nueva)+"/preguntas")

@app.route("/ir_a_ultima_encuesta", methods=['GET'])
def ir_a_ultima_encuesta():
    if db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first() == None:
        return redirect("/survey/1/preguntas")
    else:
        id_ultima_encuesta = db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first().id_encuesta
        return redirect("/survey/"+str(id_ultima_encuesta)+"/preguntas")

@app.route("/crear_encuesta", methods=['POST'])
def crear_encuesta():
    if request.method == 'POST':
        titulo = request.form.get("title-form")
        descripcion = request.form.get("description-form")
        encuesta_aux = Encuesta(titulo=titulo, descripcion=descripcion,fecha_inicio=date.today(),activa=True)
        db.session.add(encuesta_aux)
        db.session.commit()
        return redirect("/")

@app.route("/survey/")
@app.route("/survey/<int:id>/")
@app.route("/survey/<int:id>/<string:section>")
def Survey(id,section="preguntas"):
    # Tarea 1: Si se ingresa con la ruta /survey/ lo que hay que hacer es consultar el ultimo id creado de encuesta (Traerlo y almacenarlo en una var).
    # Tarea 2: Si se ingresa con la ruta /survey/id se debe preguntar a la base de datos si el id existe. Si existe se trae la info de la encuesta.
    if db.session.query(Encuesta).filter_by(id_encuesta = id).first() == None:
        #if id > 1: (Si no existe forzar redireccionamiento a la que sigue))
        #    return redirect("/")
        dataSurvey = {}
        return render_template("admin/survey.html", data={
            "options": ["Preguntas", "Respuestas", "Configuración"],
            "selected": section,
            "id": id,
            "dataSurvey": dataSurvey
            }
        )
    else:
        dataSurvey = {
            "id": id,
            "title": db.session.query(Encuesta).filter_by(id_encuesta = id).first().titulo,
            "description": db.session.query(Encuesta).filter_by(id_encuesta = id).first().descripcion,
            # "questions": [
            #     {
            #         "id": "1",
            #         "statement": "holaloquito",
            #         "type": "alternativa",
            #         "alternatives": ["Opcion1", "Opcion2", "Opcion3", "Opcion4"]
            #     },
            #     {
            #         "id": "2",
            #         "statement": "¿Cuantos años tienes?",
            #         "type": "desarrollo",
            #         "alternatives": []
            #     }
            # ]
        }
        return render_template("admin/survey.html", data={
            "options": ["Preguntas", "Respuestas", "Configuración"],
            "selected": section,
            "id": id,
            "dataSurvey": dataSurvey
            }
        )
