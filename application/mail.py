from flask_mail import Mail, Message
from flask import current_app as app
from .models import *
import base64
class Send_Mail:

    mails = []

    #Lista de mails para hacer testing:
    #users = {'ld.aravena@gmail.com', 'laravena2017@udec.cl', 'laravena2017@inf.udec.cl'}

    #Configuraciones del servidor de mail
    app.config['MAIL_SERVER']= 'smtp-mail.outlook.com'
    app.config['MAIL_PORT']= 587
    app.config['MAIL_USE_TLS']= True
    app.config['MAIL_USE_SSL']= False
    app.config['MAIL_USERNAME']= 'team1is2@outlook.com'
    app.config['MAIL_PASSWORD']= 'is2team1'
    app.config['MAIL_DEFAULT_SENDER'] = 'team1is2@outlook.com'
    #app.config['MAIL_MAX_EMAILS'] = 100
  
    def get_mails(self):

        record = db.session.query(Encuestado).filter_by(activo=True).all()
        for rec in record:
            self.mails.append(rec.email)

    #Falta testear
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


    def send_mail(self, id_survey):

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
