from cgitb import html
from email import message
from flask_mail import Mail, Message
from flask import current_app as app
from .models import *
import base64
from datetime import date
class Send_Mail:
    
    #Lista de mails
    mails = []

    #Configuraciones del servidor de mail
    app.config['MAIL_SERVER']= 'smtp-mail.outlook.com'
    app.config['MAIL_PORT']= 587
    app.config['MAIL_USE_TLS']= True
    app.config['MAIL_USE_SSL']= False
    app.config['MAIL_USERNAME']= 'team1is2@outlook.com'
    app.config['MAIL_PASSWORD']= 'is2team1'
    app.config['MAIL_DEFAULT_SENDER'] = 'team1is2@outlook.com'
    #app.config['MAIL_MAX_EMAILS'] = 100
    
    #Obtienen mails desde la base de datos
    def get_mails(self):

        self.mails.clear()
        record = db.session.query(Encuestado).filter_by(activo=True).all()
        
        for rec in record:
            self.mails.append(rec.email)

    #Obtiene nombre desde la base de datos, si el encuestado está registrado
    def get_name(self, email):

        record = db.session.query(Registrado).filter_by(email=email).first()

        if record != None:
            saludo = "Estimado/a "

            if(record.genero == "M"):
                saludo = "Estimado "
            
            elif(record.genero == "F"):
                saludo = "Estimada "
            
            nombre = (saludo + record.nombre + " " + record.apellidos + ":")          
            return nombre
        else:
            nombre = ("Estimado/a " + email + ":")
            return nombre

    def encode_link(self, str):
        str_bytes = str.encode("ascii")
        base_bytes = base64.b64encode(str_bytes)
        return base_bytes.decode("ascii")

    def decode_link(self, str):
        base_bytes = str.encode("ascii")
        str_bytes = base64.b64decode(base_bytes)
        return str_bytes.decode("ascii")

    def actualizar_asignados(self, id_survey):
        
        total = len(self.mails)
        encuesta = db.session.query(Encuesta).filter_by(id_encuesta = id_survey).first()

        if (total > encuesta.total_asignados):
            encuesta.total_asignados = total
            db.session.commit()

    #Método para enviar encuestas
    def send_survey(self, id_survey):

        encuesta = db.session.query(Encuesta).filter_by(id_encuesta = id_survey).first()

        if(encuesta == None):
            return(print("Encuesta no existe\n"))

        #Si la encuesta no se ha enviado
        if(encuesta.total_asignados == 0):

            self.get_mails()
            mail = Mail(app)
            mail.init_app(app)

            with mail.connect() as conn:

                for user in self.mails: 
                    
                    mail_coded = self.encode_link(user)
                    nombre = self.get_name(user)

                    dt = date.today()
                    current_date = dt.strftime("%d/%m/%Y")

                    if (encuesta.asunto_mail == None or encuesta.asunto_mail == ""):
                        subject = "Encuesta UdecSurvey"
                    
                    else:
                        subject = encuesta.asunto_mail

                    link_survey = "http://localhost:5001/answer_survey/"+mail_coded+"/"+ str(id_survey)

                    link_unsubscribe = "http://localhost:5001/unsubscribe/"+mail_coded

                    html_header = '<!DOCTYPE html>  <head> <style> * { margin: 0; padding: 0; border: 0;} body { font-family: "sans-serif"; background-color: #d8dada; font-size: 19px; max-width: 800px; margin: 0 auto; padding: 3%;}img { max-width: 100%; } header { width: 98%; } #wrapper { background-color: #f0f6fb;} h2, p { margin: 3%; } .btn { margin: 0 2% 4% 0; display: block; width: 20%; margin-left: 40%; margin-right: 30%; background-color: #1a5ba7; color: #f6faff; text-decoration: none; font-weight: 800; padding: 8px 12px; border-radius: 8px; letter-spacing: 2px; text-align: center} hr { height: 1px; background-color: #303840; clear: both; width: 96%; margin: auto; } #contact { text-align: center; padding-bottom: 3%; line-height: 16px; font-size: 12px; color: #303840; } </style> </head> <body> <div id="wrapper"> <div id="banner"> <img src="https://raw.githubusercontent.com/mellokx/Proyecto-Semestral-IS2/master/application/static/resources/banner_mail_udecsurvey.png" alt="UdeCSurvey" /> </div> <div class="one-col">'
                    
                    html_name = '<h2>%s</h2>' % nombre

                    if(encuesta.mensaje_mail == None or encuesta.mensaje_mail == ""):
                        mensaje_mail = 'Te invitamos a participar en la encuesta de estudios públicos. Tu participación es importante para nosotros.'
                        
                    else:
                        mensaje_mail = encuesta.mensaje_mail

                    html_body = '<p> %s </p>' %mensaje_mail

                    html_link = '</p><a href=%s class="btn">Ir a Encuesta</a> <hr />' %link_survey

                    html_footer = '<footer> <p id="contact">  Has sido seleccionado para recibir estas encuestas periódicamente <br /> <a href=%s> Dejar de recibir encuestas </a> <br /> <br /> %s &bull; Concepción - Chile  </p> </footer> </div> </div> </body> </html>' %(link_unsubscribe, current_date)
                    
                    message_html = html_header + html_name + html_body + html_link + html_footer
                  
                    msg = Message(recipients=[user], subject=subject)
                    msg.html = message_html

                    conn.send(msg)

                    # Asocia el encuestado con la encusta que ha contestado
                    encuestar_aux = Encuestar.insert().values(
                         id_encuesta=encuesta.id_encuesta, 
                         email=user,
                         contestada=False, fecha_envio=date.today())

                    db.engine.execute(encuestar_aux)
                    db.session.commit()


            self.actualizar_asignados(id_survey)
        
        else:
            return(print("Encuesta ya enviada"))

    #Método para enviar mail de recuperación de contraseña
    def send_code(self, user, code):
        
        #Comprueba que exista el mail en la base de datos
        is_admin = db.session.query(Admin).filter_by(email = user).first()
        is_register = db.session.query(Registrado).filter_by(email = user).first()

        #Si existe el mail
        if(is_admin != None or is_register != None):

            #Obtiene el nombre del usuario
            if(is_admin != None):
                name = "Estimado/a " + is_admin.nombre + ":"
            
            elif(is_register != None):
                name = self.get_name(is_register.email)

            dt = date.today()
            current_date = dt.strftime("%d/%m/%Y")
            
            html_header = '<!DOCTYPE html>  <head> <style> * { margin: 0; padding: 0; border: 0;} body { font-family: "sans-serif"; background-color: #d8dada; font-size: 19px; max-width: 800px; margin: 0 auto; padding: 3%;}img { max-width: 100%; } header { width: 98%; } #wrapper { background-color: #f0f6fb;} h2, p { margin: 3%; } .btn { margin: 0 2% 4% 0; display: block; width: 20%; margin-left: 40%; margin-right: 30%; background-color: #1a5ba7; color: #f6faff; text-decoration: none; font-weight: 800; padding: 8px 12px; border-radius: 8px; letter-spacing: 2px; text-align: center} hr { height: 1px; background-color: #303840; clear: both; width: 96%; margin: auto; } #contact { text-align: center; padding-bottom: 3%; line-height: 16px; font-size: 12px; color: #303840; } </style> </head> <body> <div id="wrapper"> <div id="banner"> <img src="https://raw.githubusercontent.com/mellokx/Proyecto-Semestral-IS2/master/application/static/resources/banner_mail_udecsurvey.png" alt="UdeCSurvey" /> </div> <div class="one-col">'

            html_name = '<h2>%s</h2>' % name

            html_body = '<p>Para recuperar su contraseña del sistema UdecSurvey por favor ingrese el siguiente código: </p> <center> <h2 style = "letter-spacing:4px;"> %s </h2> </center> <p>Si no ha solicitado recuperación de contraseña, ignore este mensaje</p>' % code

            html_footer = '<footer> <p id="contact">  UdecSurvey <br /> %s &bull; Concepción - Chile  </p> </footer> </div> </div> </body> </html>' % current_date

            message_html = html_header + html_name + html_body + html_footer

            #Manda el mail
            mail = Mail(app)
            mail.init_app(app)

            subject = "Recuperación de Contraseña UdecSurvey"

            msg = Message(recipients=[user], subject=subject)
            msg.html = message_html

            mail.send(msg)

            return ("Email enviado")
        
        else:
            return ("Email no existe")
