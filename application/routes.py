"""Rutas de la aplicacion"""
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
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
    # from werkzeug.security import generate_password_hash
    # print(generate_password_hash("1234"))
    # return redirect(url_for("login"))
    return render_template("login.html")

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
                if logged_user.rol == "admin":
                    return redirect(url_for("dashboard_admin"))
                else:
                    return redirect(url_for("dashboard_user"))
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

@app.route("/register")
def register():
   return render_template("register.html")

@app.route("/register_user" ,methods=['POST'])
def register_user():
    
    dataRegister = {
        "email" : request.form['email'],
        "password" : request.form['password'],
        "name" : request.form['name'],
        "apellido" : request.form['surname'],
        "rut" : request.form['rut'],
        "genero" : request.form.get("gender"),
        "fecha_nacimiento" : request.form['date']
    }
    
    return registrar_encuestado(dataRegister)

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


@app.route("/create_survey", methods=['POST'])
@login_required
@admin_required
def create_survey():
    if request.method == 'POST':
        surveyData = json.loads(request.form.get("surveyData"))
        return guardar_encuesta(surveyData,current_user.id)


@app.route("/modify_survey", methods=['POST'])
@login_required
@admin_required
def modify_survey():
    if request.method == 'POST':
        surveyData = json.loads(request.form.get("surveyData"))
        return modificar_encuesta(surveyData)


@app.route("/delete_survey", methods=['POST'])
@login_required
@admin_required
def delete_survey():
    if request.method == 'POST':
        response = json.loads(request.form.get("response"))
        return eliminar_encuesta(response["id_survey"])

@app.route("/delete_user", methods=['POST'])
@login_required
@admin_required
def delete_user():
    if request.method == 'POST':
        response = json.loads(request.form.get("response"))
        return "USUARIO ELIMINADO"

@app.route("/state_user", methods=['POST'])
@login_required
@admin_required
def state_user():
    if request.method == 'POST':
        response = json.loads(request.form.get("response"))
        cambiar_estado_invitado(response)
        return response


@app.route("/responder_encuesta", methods=['POST'])
def responder_encuesta():
    if request.method == 'POST':
        responses = json.loads(request.form.get("responses"))
        return guardar_respuesta(responses)
    return redirect("/")

@app.route("/agregar_usuario", methods=['POST'])
def agregar_usuario():
    if request.method == 'POST':
        responses = json.loads(request.form.get("response"))
        agregar_invitado(responses)
        return responses
    return redirect("/")

@app.route("/cambiar_estado_survey", methods=['POST'])
def cambiar_estado_survey():
    if request.method == 'POST':
        responses = json.loads(request.form.get("response"))
        cambiar_estado_encuesta(responses)
        return responses


@app.route("/survey/")
@app.route("/survey/<int:id_encuesta>/")
@app.route("/survey/<int:id_encuesta>/<string:section>")
@login_required
@admin_required
def Survey(id_encuesta, section="preguntas"):

    if section == "preguntas":
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

                "url": "survey",
                "options": ["Preguntas", "Respuestas", "Usuarios", "Configuración"],
                "selected": section,
                "id": id_encuesta,
                "dataSurvey": dataSurvey,
                "textButton": "Guardar"
            }
            )
        else:
            dataSurvey = crear_dataSurvey(id_encuesta)
            return render_template("admin/survey.html", data={

                "url": "survey",
                "options": ["Preguntas", "Respuestas", "Usuarios", "Configuración"],
                "selected": section,
                "id": id_encuesta,
                "dataSurvey": dataSurvey,
                "textButton": "Modificar"
            }
            )
    elif section == "respuestas":

        return render_template("admin/survey.html", data={
        "url": "survey",
        "options": ["Preguntas", "Respuestas", "Usuarios", "Configuración"],
        "selected": section,
        "id": id_encuesta,
        "textButton": "Modificar",
        "dataAnswers" : obtener_respuestas_opcion(id_encuesta)
        }
        )
    elif section == "usuarios":
        return render_template("admin/survey.html", data={
        "url": "survey",
        "options": ["Preguntas", "Respuestas", "Usuarios", "Configuración"],
        "selected": section,
        "id": id_encuesta,
        "textButton": "Modificar",
        "dataUsers" : obtener_encuestados_responden(id_encuesta),
        }
        )
    elif section == "configuración":
        return render_template("admin/survey.html", data={
        "url": "survey",
        "options": ["Preguntas", "Respuestas", "Usuarios", "Configuración"],
        "selected": section,
        "id": id_encuesta,
        "textButton": "Modificar",
        }
        )

#Ruta de respuesta de encuesta   
@app.route("/answer_survey/<string:url>/<int:id_encuesta>")
def answer_survey(url, id_encuesta):

    if (len(url) % 4 != 0 or len(url) == 0):
        print("Error 404")
        return redirect("/invalid")
    
    email = decodificar_mail(url)

    #Si no existe mail en la base de datos
    if (db.session.query(Encuestado).filter_by(email = email) == None):
        print("Error 404")
        return redirect("/invalid")

    encuesta = db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first()

    #Si la encuesta existe
    if encuesta != None:

        #Comprobar fecha encuesta y si ya fue respondida por usuario
        if (comprobar_encuestado_encuesta(id_encuesta, email) == True):
            return ("Encuesta no disponible")
            return redirect("/")

        #Si la encuesta está activa
        if (encuesta.activa == True):

            dataSurvey = crear_dataSurvey(id_encuesta)
            print(dataSurvey)
            return render_template("user/answer_survey.html", data={

                "selected": "answer",
                "dataSurvey":dataSurvey, 
                "encuestado": email,
                "type": comprobar_tipo_encuestado(email),
                "role":'encuestado',
                "title" : dataSurvey.title
                })
        else:
            return ("Encuesta no está activa")
    else:
        return ("Encuesta no existe")
        #return redirect("/")

# Enviar mails con encuestas
@app.route("/mail_sent", methods=['POST'])
def send_mail():
    if request.method == 'POST':
        response = json.loads(request.form.get("response"))
        print(response.get("id_survey"))
        
        send_mail = Send_Mail()
        send_mail.send_survey(response.get("id_survey"))
        
        return "PUBLICADA CORRECTAMENTE"

# Enviar mail de recuperación de contraseña
@app.route("/password_reset", methods=['POST'])
def password_reset():
    if request.method == 'POST':

        user_mail = "user@mail.com"
        code = "123456"

        send_mail = Send_Mail()
        return (send_mail.send_code(user_mail, code))

@app.route("/dashboard_admin/")
@app.route("/dashboard_admin/<string:section>")
@app.route("/dashboard_admin/<string:section>/<string:active>")
@login_required
@admin_required
def dashboard_admin(section="encuestas",active="false"):
    ##ACA TRAER TODAS LAS ENCUESTAS CREADAS POR UN USUARIO ADMIN (?)

    if section == "encuestas":
        return render_template("admin/dashboardAdmin.html", data={

        "url": "dashboard_admin",
        "options": ["Encuestas", "Usuarios"],
        "selected": section,
        "active": active,
        "dataSurveys": obtener_encuestas(),
        "dataChart": obtener_cantidad_registrados_e_invitados(),
        "title" : "Bienvenido " + current_user.nombre
        }
        )
    elif section == "usuarios":
        return render_template("admin/dashboardAdmin.html", data={

        "url": "dashboard_admin",
        "options": ["Encuestas", "Usuarios"],
        "selected": section,
        "active": active,
        "dataUsers": obtener_usuarios(),
        "title" : "Bienvenido " + current_user.nombre
        }
        )
    
@app.route("/aumentar_visita", methods=['POST'])
def aumentar_visita():
    if request.method == 'POST':
        response = json.loads(request.form.get("id_survey"))

        print(response)
        
        return aumentar_visitas(response)  

@app.route("/dashboard_user/")
@login_required
@registrado_required
def dashboard_user():
    ##ACA TRAER TODAS LAS ENCUESTAS CREADAS POR UN USUARIO ADMIN (?)
    return render_template("user/dashboardUser.html",data={
        "url": "dashboard_user",
        "options": [],
        "role":'encuestado'
        })

#Desunscribe encuestados  
@app.route("/unsubscribe/<string:url>")
def unsubscribe_mail(url):

    if (len(url) % 4 != 0 or len(url) == 0):
        print("Error 404")
        return redirect("/invalid")
    
    email = decodificar_mail(url)

    return desunscribir_encuestado(email)

@app.route("/my_profile")
@login_required
def my_profile():

    return render_template("myProfile.html", data={
    "url": "dashboard_user",
    "options": [],
    "selected": "",
    "role": current_user.rol,
    "title" : "Perfil de " + current_user.nombre 
    })
    