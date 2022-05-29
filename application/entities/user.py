from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, email, password, nombre, rol) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.nombre = nombre
        self.rol = rol

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)