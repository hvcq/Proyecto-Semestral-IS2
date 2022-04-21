"""Data models."""
from . import db

class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nombre = db.Column(db.String(100))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))