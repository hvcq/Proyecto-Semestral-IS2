from flask_mail import Mail, Message

from flask import current_app as app
class Send_Mail:

    mails = []

    app.config['MAIL_SERVER']= 'smtp-mail.outlook.com'
    app.config['MAIL_PORT']= 587
    app.config['MAIL_USE_TLS']= True
    app.config['MAIL_USE_SSL']= False
    app.config['MAIL_USERNAME']= 'team1is2@outlook.com'
    app.config['MAIL_PASSWORD']= 'is2team1'
    app.config['MAIL_DEFAULT_SENDER'] = 'team1is2@outlook.com'

    #def __init__(self):
  
    def recipients(self, recipient):

        self.mails.append(recipient)

    def send_mail(self):

        mail = Mail(app) # Crea el objeto 'mail'
        mail.init_app(app) # Inicia el objeto 'mail'
        msg = Message(subject='Saludos 7', recipients=self.mails, body='Mail de prueba 7, saludos'
        )
        mail.send(msg)

