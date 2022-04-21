"""Data models."""
from sqlalchemy import Table, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from time import timezone
from . import db

class Admin(db.Model):
    __tablename__ = 'admin'
    id_admin = Column(Integer,primary_key=True,autoincrement=True)
    nombre = Column(String(100), nullable = False)
    email = Column(String(50), nullable = False)

class Encuesta(db.Model):
    __tablename__ = 'encuesta'
    id_encuesta = Column(Integer,primary_key=True,autoincrement=True)
    titulo = Column(String(100), nullable = False)
    descripcion = Column(String(500), nullable = False)
    fecha_inicio = Column(Date())
    fecha_fin = Column(Date())
    activa = Column(Boolean, nullable=False)
    comentario = Column(String(500))

crea_encuesta = Table('crea_encuesta',db.Model.metadata,
    Column('id_admin',ForeignKey('admin.id_admin'), primary_key=True),
    Column('id_encuesta',ForeignKey('encuesta.id_encuesta'), primary_key=True)
)