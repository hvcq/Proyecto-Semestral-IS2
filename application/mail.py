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
            return record.nombre
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

    def send_mail(self, id_survey):

        self.get_mails()
        mail = Mail(app)
        mail.init_app(app)

        with mail.connect() as conn:

            for user in self.mails: 
                
                mail_coded = self.encode_link(user)
                
                nombre = self.get_name(user)

                subject ="Saludos "+ nombre
                message = "Estimado "+ nombre +" :\n Gracias por participar en el centro de estudios públicos al contestar la siguiente encuesta: \nhttp://localhost:3000/"+ mail_coded + "/" +id_survey+ "/"

                msg = Message(recipients=[user], body=message, subject=subject)

                conn.send(msg)
