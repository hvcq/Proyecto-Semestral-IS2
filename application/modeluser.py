from ast import Mod
from .entities.user import User
from .models import *

class ModelUser():
    __rol_actual = "desconocido"
    __email_encuestado = "sin_email"

    @classmethod
    def login(self, user):
        try:
            """Comprobamos si existe el email del usuario para manejar error en routes.py"""
            admin = db.session.query(Admin).filter_by(email=user.email).first()
            if admin != None:
                user = User(admin.id_admin, admin.email, User.check_password(admin.password, user.password), admin.nombre, "admin")
                ModelUser.__rol_actual = "admin"
                return user
            else:
                registrado = db.session.query(Registrado).filter_by(email=user.email).first()
                if registrado != None:
                    user = User(registrado.id_registrado, registrado.email, User.check_password(registrado.password, user.password), registrado.nombre, "registrado")
                    ModelUser.__rol_actual = "registrado"
                    return user
                else:
                    encuestado = db.session.query(Encuestado).filter_by(email=user.email).first()
                    if encuestado != None:
                        user = User(0, encuestado.email, True, "invitado", "encuestado")
                        ModelUser.__rol_actual = "encuestado"
                        ModelUser.__email_encuestado = encuestado.email
                        return user
                    else:
                        return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, id):
        try:
            if ModelUser.__rol_actual == "admin":
                admin = db.session.query(Admin).filter_by(id_admin=id).first()
                if admin != None:
                    return User(id, admin.email, None, admin.nombre, "admin")
                else:
                    return None
            elif ModelUser.__rol_actual == "registrado":
                registrado = db.session.query(Registrado).filter_by(id_registrado=id).first()
                if registrado != None:
                    return User(id, registrado.email, None, registrado.nombre, "registrado")
                else:
                    return None
            elif ModelUser.__rol_actual == "encuestado":
                encuestado = db.session.query(Encuestado).filter_by(email=ModelUser.__email_encuestado).first()
                if encuestado != None:
                    return User(id, encuestado.email, None, "invitado", "encuestado")
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)