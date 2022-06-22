from flask_mail import Mail, Message
from flask import current_app as app
from .models import *
import base64
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
            
            nombre = (saludo + record.nombre + " " + record.apellidos)          
            return nombre
        else:
            nombre = "Estimado/a " + email
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

                    subject = encuesta.asunto_mail

                    link_survey = "http://localhost:5001/answer_survey/"+mail_coded+"/"+ str(id_survey)

                    link_unsubscribe = "http://localhost:5001/unsubscribe/"+mail_coded

                    html_name = '<p><span style="font-family:Arial,Helvetica,sans-serif"><span style="font-size:16px">%s:</span></span></p>' % nombre
                    html_body = '<p><span style="font-size:16px"><span style="font-family:Arial,Helvetica,sans-serif">%s</span></span></p>' % encuesta.mensaje_mail
                    html_link = '<p><span style="font-size:16px"><a href="%s">%s</a></span></p>' % (link_survey, link_survey)
                    html_bye = '<p><span style="font-size:16px">Saludos</span></p> <p><span style="font-size:16px">UdecSurvey</span></p>'
                    html_unsubscribe = '<p><span style="font-size:9px">Si no desea recibir correos con encuestas <a href=%s>haga clic aqu&iacute; </a></span></p>' % link_unsubscribe

                    message_html = html_name + html_body + html_link + html_bye + html_unsubscribe
                    # subject = ""
                    # message = ""

                    # if encuesta.asunto_mail == "":
                    #     subject = "Default"
                    # else:
                    #     subject = encuesta.asunto_mail
                    
                    # if encuesta.mensaje_mail == "":
                    #     message = nombre +" :\nGracias por participar en el estudio público al contestar la siguiente encuesta del sistema UdecSurvey: \n\nhttp://localhost:3000/answer_survey/"+ mail_coded + "/" +str(id_survey)
                    # else:
                    #     message = nombre +" :\n" + encuesta.mensaje_mail + "\n\nhttp://localhost:3000/answer_survey/"+ mail_coded + "/" +str(id_survey)

                    msg = Message(recipients=[user], subject=subject)
                    msg.html = message_html

                    conn.send(msg)

                    # Asocia el encuestado con la encusta que ha contestado
                    from datetime import date
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
            
            name = "Usuario"

            #Obtiene el nombre del usuario
            if(is_admin != None):
                name = is_admin.nombre
            
            elif(is_register != None):
                name = is_register.nombre + " " + is_register.apellidos
            
            #Manda el mail
            mail = Mail(app)
            mail.init_app(app)

            subject = "Recuperación de Contraseña"
            message = "Estimado" + name + ": \nPara recuperar su contraseña ingrese el siguiente código en la página de recuperación:\n\n" + code 

            msg = Message(recipients=[user],body=message, subject=subject)
            mail.send(msg)

            print("Email enviado")
        
        else:
            print("Email no existe")
