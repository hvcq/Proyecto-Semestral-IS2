"""Rutas de la aplicacion"""
from datetime import datetime,date
from operator import length_hint

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models import *

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
        """Consulta para obtener datos de preguntas de desarrollo"""
        ids_preguntas_desarrollo = []
        numeros_preguntas_desarrollo = []
        enunciado_preguntas_desarrollo = []
        comentario_preguntas_desarrollo = []
        if db.session.query(Desarrollo_Encuesta).filter_by(id_encuesta = id).first() != None:
            tuplas_desarrollo_encuesta = db.session.query(Desarrollo_Encuesta).filter_by(id_encuesta = id).all()
            for tupla_desarrollo_encuesta in tuplas_desarrollo_encuesta:
                ids_preguntas_desarrollo.append(tupla_desarrollo_encuesta.id_pregunta_desarrollo)
            tuplas_pregunta_desarrollo = db.session.query(Pregunta_Desarrollo).filter(Pregunta_Desarrollo.id_pregunta_desarrollo.in_(ids_preguntas_desarrollo)).all()
            for tupla_pregunta_desarrollo in tuplas_pregunta_desarrollo:
                numeros_preguntas_desarrollo.append(tupla_pregunta_desarrollo.numero)
                enunciado_preguntas_desarrollo.append(tupla_pregunta_desarrollo.enunciado)
                comentario_preguntas_desarrollo.append(tupla_pregunta_desarrollo.comentario)
            print("numeros_pd") #pd -> pregunta desarrollo
            print(numeros_preguntas_desarrollo)
            print("enunciados_pd")
            print(enunciado_preguntas_desarrollo)
            print("comentarios_pd")
            print(comentario_preguntas_desarrollo)
        
        """Consulta para obtener datos de preguntas de alternativas"""
        ids_preguntas_alternativas = []
        numeros_preguntas_alternativas = []
        enunciado_preguntas_alternativas = []
        comentario_preguntas_alternativas = []
        ids_opciones = []
        string_opciones = []
        if db.session.query(Alternativa_Encuesta).filter_by(id_encuesta = id).first() != None:
            tuplas_alternativa_encuesta = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta = id).all()
            for tupla_alternativa_encuesta in tuplas_alternativa_encuesta:
                ids_preguntas_alternativas.append(tupla_alternativa_encuesta.id_pregunta_alternativa)
            tuplas_pregunta_alternativa = db.session.query(Pregunta_Alternativa).filter(Pregunta_Alternativa.id_pregunta_alternativa.in_(ids_preguntas_alternativas)).all()
            for tupla_pregunta_alternativa in tuplas_pregunta_alternativa:
                numeros_preguntas_alternativas.append(tupla_pregunta_alternativa.numero)
                enunciado_preguntas_alternativas.append(tupla_pregunta_alternativa.enunciado)
                comentario_preguntas_alternativas.append(tupla_pregunta_alternativa.comentario)
            print("numeros_pa") # pa -> pregunta alternativa
            print(numeros_preguntas_alternativas)
            print("enunciados_pa")
            print(enunciado_preguntas_alternativas)
            print("comentarios_pa")
            print(comentario_preguntas_alternativas)
            for id_pregunta_alternativa in ids_preguntas_alternativas:
                if db.session.query(Alternativas).filter_by(id_pregunta_alternativa = id_pregunta_alternativa).first() != None:
                    tuplas_alternativas_aux = db.session.query(Alternativas).filter_by(id_pregunta_alternativa = id_pregunta_alternativa).all()
                    for tupla_alternativa in tuplas_alternativas_aux:
                        ids_opciones.append(tupla_alternativa.id_opcion)
            print("ids opciones")
            print(ids_opciones)
            tuplas_opcion = db.session.query(Opcion).filter(Opcion.id_opcion.in_(ids_opciones)).all()
            for tupla_opcion in tuplas_opcion:
                string_opciones.append(tupla_opcion.opcion)
            print("string opciones")
            print(string_opciones)
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
