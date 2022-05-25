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

    #def __init__(self):
  
    def get_mails(self):
        print("\n\nMails:\n\n")

        record = db.session.query(Encuestado).filter_by(activo=True).all()
        for rec in record:
            self.mails.append(rec.email)

        for i in self.mails:
            print (i + "\n")


    def encode_link(self, str):
        str_bytes = str.encode("ascii")
        base_bytes = base64.b64encode(str_bytes)
        return base_bytes.decode("ascii")

    def decode_link(self, str):
        base_bytes = str.encode("ascii")
        str_bytes = base64.b64decode(base_bytes)
        return str_bytes.decode("ascii")

    def send_mail(self):

        mail = Mail(app)
        mail.init_app(app)

        with mail.connect() as conn:

            #modo testing
            for user in self.mails: 
                mail_coded = self.encode_link(user)
                mail_decoded = self.decode_link(mail_coded)
                
                #print("CODED: "+mail_coded)
                #print("DECODED: "+mail_decoded)

                subject ="Saludos "+ user
                message = "Hola "+ user +" Este es el link codificado: \nhttp://localhost:3000/test_mail/"+ mail_coded + "\n\ncorreo original: " + mail_decoded + "\n\nSaludos"

                msg = Message(recipients=[user], body=message, subject=subject)

                conn.send(msg)
