"""Rutas de la aplicacion"""
from .consultas import *
from .estructuraInterfaz import *
import json

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models import *

#TEMPORAL
from .mail import *

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


@app.route("/ir_a_crear_nueva_encuesta", methods=['GET'])
def crea_nueva_encuesta():
    if db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first() == None:
        return redirect("/survey/1/preguntas")
    else:
        id_ultima_encuesta = db.session.query(Encuesta).order_by(
            Encuesta.id_encuesta.desc()).first().id_encuesta
        id_nueva = id_ultima_encuesta + 1
        return redirect("/survey/"+str(id_nueva)+"/preguntas")


@app.route("/ir_a_ultima_encuesta", methods=['GET'])
def ir_a_ultima_encuesta():
    if db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first() == None:
        return redirect("/survey/1/preguntas")
    else:
        id_ultima_encuesta = db.session.query(Encuesta).order_by(
            Encuesta.id_encuesta.desc()).first().id_encuesta
        return redirect("/survey/"+str(id_ultima_encuesta)+"/preguntas")


@app.route("/crear_encuesta", methods=['POST'])
def crear_encuesta():
    if request.method == 'POST':
        surveyData = json.loads(request.form.get("surveyData"))
        return guardar_encuesta(surveyData)
    return redirect("/")


@app.route("/responder_encuesta", methods=['POST'])
def responder_encuesta():
    if request.method == 'POST':
        responses = json.loads(request.form.get("responses"))
        return guardar_respuesta(responses)
    return redirect("/")


@app.route("/survey/")
@app.route("/survey/<int:id_encuesta>/")
@app.route("/survey/<int:id_encuesta>/<string:section>")
def Survey(id_encuesta, section="preguntas"):
    if db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first() == None:
        # if id > 1: (Si no existe forzar redireccionamiento a la que sigue))
        #    return redirect("/")
        dataSurvey = {
            "id": id_encuesta,
            "title": "",
            "description": "",
            "questions": []
        }
        return render_template("admin/survey.html", data={
            "options": ["Preguntas", "Respuestas", "Configuración"],
            "selected": section,
            "id": id_encuesta,
            "dataSurvey": dataSurvey,
            "textButton": "Guardar"
        }
        )
    else:
        dataSurvey = crear_dataSurvey(id_encuesta)
        return render_template("admin/survey.html", data={
            "options": ["Preguntas", "Respuestas", "Configuración"],
            "selected": section,
            "id": id_encuesta,
            "dataSurvey": dataSurvey,
            "textButton": "Modificar"
        }
        )


@ app.route("/answer_survey/<int:id_encuesta>")
def answer_survey(id_encuesta):
    if db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first() != None:
        dataSurvey = crear_dataSurvey(id_encuesta)
        print(dataSurvey)
        return render_template("user/answer_survey.html", data=dataSurvey)
    else:
        print("Error: Encuesta no existente")
        return redirect("/")

# Enviar mails
@app.route("/mail_sent", methods=['POST'] )
def send_mail():
    if request.method == 'POST':
        #Crea el objeto send_mail
        send_mail = Send_Mail()

        #Metodo para enviar los mails
        send_mail.send_mail()
        return "correos enviados!"

@app.route("/test_mail/<coded_mail>")
def decode_mail(coded_mail):
    obj = Send_Mail()
    mail = obj.decode_link(coded_mail) #Decodificacion funciona bien

    #No testeado
    rec = db.session.query(Encuestado).filter_by(email=mail).all()
    if rec != None:
        if rec.activo == True:
            return "Mail Valido"

