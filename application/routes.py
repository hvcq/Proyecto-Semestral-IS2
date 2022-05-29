"""Rutas de la aplicacion"""
from flask_login import LoginManager, login_user, logout_user, login_required
from .consultas import *
from .estructuraInterfaz import *
from .modeluser import *
from .decorators import *
import json

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models import *

#TEMPORAL
from .mail import *

login_manager_app=LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

@app.route("/")
def index():
    # return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['email'], request.form['password'],"","indefinido")
        logged_user = ModelUser.login(user)
        if logged_user != None:
            print(logged_user.email)
            if logged_user.password:
                login_user(logged_user)
                print(logged_user.password)
                return redirect(url_for("dashboard_admin"))
            else:
                # aqui deberia desplegar un mensaje con el error
                print("error: password no coincide")
                return render_template("login.html")
        else:
            # aqui deberia desplegar un mensaje con el error
            print("error: email no existe")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/ir_a_crear_nueva_encuesta", methods=['GET'])
@login_required
@admin_required
def crea_nueva_encuesta():
    if db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first() == None:
        return redirect("/survey/1/preguntas")
    else:
        id_ultima_encuesta = db.session.query(Encuesta).order_by(
            Encuesta.id_encuesta.desc()).first().id_encuesta
        id_nueva = id_ultima_encuesta + 1
        return redirect("/survey/"+str(id_nueva)+"/preguntas")


@app.route("/ir_a_ultima_encuesta", methods=['GET'])
@login_required
@admin_required
def ir_a_ultima_encuesta():
    if db.session.query(Encuesta).order_by(Encuesta.id_encuesta.desc()).first() == None:
        return redirect("/survey/1/preguntas")
    else:
        id_ultima_encuesta = db.session.query(Encuesta).order_by(
            Encuesta.id_encuesta.desc()).first().id_encuesta
        return redirect("/survey/"+str(id_ultima_encuesta)+"/preguntas")


@app.route("/crear_encuesta", methods=['POST'])
@login_required
@admin_required
def crear_encuesta():
    if request.method == 'POST':
        surveyData = json.loads(request.form.get("surveyData"))
        guardar_encuesta(surveyData)
        return redirect(url_for("dashboard_admin"))
    return redirect(url_for("dashboard_admin"))

@app.route("/delete_survey", methods=['POST'])
@login_required
@admin_required
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
@login_required
@admin_required
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


@app.route("/answer_survey/<int:id_encuesta>")
def answer_survey(id_encuesta):
    if db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first() != None:
        dataSurvey = crear_dataSurvey(id_encuesta)
        print(dataSurvey)
        return render_template("user/answer_survey.html", data={
            "userData":{
                "username": "Anonimo",
                "email": "example@udec.cl",
                "role": "None",
            },
            "selected": "answer",
            "dataSurvey":dataSurvey
            })
    else:
        print("Error: Encuesta no existente")
        return redirect("/")

# Enviar mails
@app.route("/mail_sent", methods=['POST'])
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
@login_required
@admin_required
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
        "dataSurveys": obtener_encuestas()
        }
        )
