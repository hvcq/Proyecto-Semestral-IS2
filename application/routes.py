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


@app.route("/login")
def login():
    return render_template("loginPage.html", data={})


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

@app.route("/delete_survey", methods=['POST'])
def delete_survey():
    if request.method == 'POST':
        response = json.loads(request.form.get("response"))
        print(response)
        return "BORRADA CORRECTAMENTE"
        #LLAMAR AL METODO PARA GUARDAR ESTADO DE ENCUESTA


@app.route("/responder_encuesta", methods=['POST'])
def responder_encuesta():
    if request.method == 'POST':
        responses = json.loads(request.form.get("responses"))
        return guardar_respuesta(responses)
    return redirect("/")

@app.route("/cambiar_estado", methods=['POST'])
def cambiar_estado():
    if request.method == 'POST':
        response = json.loads(request.form.get("response"))
        print(response)
        return "CAMBIADO CORRECTAMENTE EL ESTADO"
        #LLAMAR AL METODO PARA GUARDAR ESTADO DE ENCUESTA


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
            "userData": {
                "username": "Benjamin Fernandez",
                "email": "bfernandez@inf.udec.cl",
                "role": "Admin",
             },
            "url": "survey",
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
            "userData": {
                "username": "Benjamin Fernandez",
                "email": "bfernandez@inf.udec.cl",
                "role": "Admin",
            },
            "url": "survey",
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
        response = json.loads(request.form.get("response"))
        print(response)
        return "PUBLICADA CORRECTAMENTE"
        #COMENTADO POR MIENTRAS PARA PROBAR QUE FUNCIONA EL LISTENER
        # #Crea el objeto send_mail:
        # send_mail = Send_Mail()

        # #Obtiene mails desde BD:
        # send_mail.get_mails()

        # #Metodo para enviar los mails:
        # #send_mail.send_mail()
        # return "correos obtenidos!"

#Ruta para testear mails activos, no activos y no existentes en la base de datos
#Desde una url codificada con base64: 
@app.route("/test_mail/<coded_mail>")
def decode_mail(coded_mail):
    obj = Send_Mail()

    #Decodifica mails desde URL:
    mail = obj.decode_link(coded_mail) 

    #Obtiene registro desde BD, segun el mail decodificado
    rec = db.session.query(Encuestado).filter_by(email=mail).first()

    #Si el mail existe:
    if rec!= None:

        #Si el mail esta activo:
        if rec.activo == True:
            return ("Mail Activo: " + rec.email)
        else:
            return ("Mail No Activo: " + rec.email)
    else:
        return "Mail No Registrado"


@app.route("/dashboard_admin/")
@app.route("/dashboard_admin/<string:section>")
@app.route("/dashboard_admin/<string:section>/<string:active>")
def dashboard_admin(section="encuestas",active="false"):
    ##ACA TRAER TODAS LAS ENCUESTAS CREADAS POR UN USUARIO ADMIN (?)
    return render_template("admin/dashboardAdmin.html", data={
        "userData": {
            "username": "Benjamin Cristobal Fernandez Vera",
            "email": "bfernandez@inf.udec.cl",
            "role": "Admin",
        },
        "url": "dashboard_admin",
        "options": ["Encuestas", "Usuarios", "Configuración"],
        "selected": section,
        "active": active,
        "dataSurveys": [
            {
                "id_survey": 0,
                "title": "Los gatos son lo mejor del mundo",
                "description": "Los gatos si tu lo piensas son lo mejor por diferentes razones. Primero son gatos, segundo son lindos",
                "start_date": "22 de julio del 2022",
                "end_date": "30 de julio del 2022",
                "active" : bool(1),
                "comentario": "",
                "visits": 200,
                "answers" : {"total":1200,"current_answers": 200}

            },
            {
                "id_survey": 1,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(0),
                "comentario": "",
                "visits": 400,
                "answers" : {"total":600,"current_answers": 400}

            },
            {
                "id_survey": 2,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(0),
                "comentario": "",
                "visits": 0,
                "answers" : {"total":0,"current_answers": 0}

            },
            {
                "id_survey": 3,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(0),
                "comentario": "",
                "visits": 600,
                "answers" : {"total":600,"current_answers": 600}

            },
            {
                "id_survey": 4,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(0),
                "comentario": "",
                "visits": 400,
                "answers" : {"total":600,"current_answers": 400}

            },
            {
                "id_survey": 5,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(1),
                "comentario": "",
                "visits": 400,
                "answers" : {"total":600,"current_answers": 400}

            },
            {
                "id_survey": 6,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(0),
                "comentario": "",
                "visits": 400,
                "answers" : {"total":600,"current_answers": 400}

            },
            {
                "id_survey": 7,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(0),
                "comentario": "",
                "visits": 400,
                "answers" : {"total":600,"current_answers": 400}

            },
            {
                "id_survey": 8,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(1),
                "comentario": "",
                "visits": 400,
                "answers" : {"total":600,"current_answers": 400}

            },
             {
                "id_survey": 9,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(0),
                "comentario": "",
                "visits": 400,
                "answers" : {"total":600,"current_answers": 400}

            },
             {
                "id_survey": 10,
                "title": "Los perros son lo mejor del mundo",
                "description": "Los perros si tu lo piensas son lo mejor por diferentes razones. Primero son perros, segundo son lindos",
                "start_date": "23 de julio del 2022",
                "end_date": "30 de agosto del 2022",
                "active" : bool(1),
                "comentario": "",
                "visits": 400,
                "answers" : {"total":600,"current_answers": 400}

            }
        ]
        }
        )

