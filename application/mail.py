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

        record = db.session.query(Encuestado).filter_by(activo=True).all()
        for rec in record:
            self.mails.append(rec.email)

    #Obtiene nombre desde la base de datos, si el encuestado está registrado
    def get_name(self, email):

        record = db.session.query(Registrado).filter_by(email=email).first()
        if record != None:
            nombre = (record.nombre + " " + record.apellidos) 
            return nombre
        else:
            return email

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

        self.get_mails()
        mail = Mail(app)
        mail.init_app(app)

        encuesta = db.session.query(Encuesta).filter_by(id_encuesta = id_survey).first()

        with mail.connect() as conn:

            for user in self.mails: 
                
                mail_coded = self.encode_link(user)
                
                nombre = self.get_name(user)
                subject = ""
                message = ""

                if encuesta.asunto_mail == "":
                    subject = "Saludos "+ nombre
                else:
                    subject = encuesta.asunto_mail
                
                if encuesta.mensaje_mail == "":
                    message = "Estimado "+ nombre +" :\nGracias por participar en el estudio público al contestar la siguiente encuesta del sistema UdecSurvey: \n\nhttp://localhost:3000/answer_survey/"+ mail_coded + "/" +str(id_survey)
                else:
                    message = "Estimado "+ nombre +" :\n" + encuesta.mensaje_mail + "\n\nhttp://localhost:3000/answer_survey/"+ mail_coded + "/" +str(id_survey)

                msg = Message(recipients=[user], body=message, subject=subject)

                conn.send(msg)

        self.actualizar_asignados(id_survey)

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
