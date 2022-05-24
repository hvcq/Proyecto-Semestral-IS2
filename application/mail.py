from flask_mail import Mail, Message
from flask import current_app as app
from .models import *
import base64
class Send_Mail:

    mails = []

    users = {'ld.aravena@gmail.com', 'laravena2017@inf.udec.cl', 'laravena2017@udec.cl'}

    #Configuraciones del servidor de mail
    app.config['MAIL_SERVER']= 'smtp-mail.outlook.com'
    app.config['MAIL_PORT']= 587
    app.config['MAIL_USE_TLS']= True
    app.config['MAIL_USE_SSL']= False
    app.config['MAIL_USERNAME']= 'team1is2@outlook.com'
    app.config['MAIL_PASSWORD']= 'is2team1'
    app.config['MAIL_DEFAULT_SENDER'] = 'team1is2@outlook.com'
    #app.config['MAIL_MAX_EMAILS'] = 100

    #def __init__(self):
  
    def get_mails(self):
        record = db.session.query(Encuestado).filter_by(activo=True).all()
        for rec in record:
            self.mails.append(rec.email)


    def encode_link(self, str):
        str_bytes = str.encode("ascii")
        base_bytes = base64.b64encode(str_bytes)
        return base_bytes.decode("ascii")

    def decode_link(self, str):
        base_bytes = str.encode("ascii")
        str_bytes = base64.decode(base_bytes)
        return str_bytes.decode("ascii")

    def send_mail(self):

        mail = Mail(app)
        mail.init_app(app)

        with mail.connect() as conn:

            for user in self.mails:
                subject ="Saludos "+ user
                message = "Hola "+ user +" Este es un el link de su encuesta: http://localhost:3000/encuesta1/"+ self.encode_link(user)+"/"

                msg= Message(recipients=[user], body=message, subject=subject)
                #print(user)

                conn.send(msg)

  
