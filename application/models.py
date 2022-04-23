"""Tablas de la base de datos"""
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

Crea_Encuesta = Table('crea_encuesta',db.Model.metadata,
    Column('id_admin',ForeignKey('admin.id_admin'), primary_key=True),
    Column('id_encuesta',ForeignKey('encuesta.id_encuesta'), primary_key=True)
)

class Pregunta_Desarrollo(db.Model):
    __tablename__ = 'pregunta_desarrollo'
    id_pregunta_desarrollo = Column(Integer,primary_key=True,autoincrement=True)
    numero = Column(Integer)
    enunciado = Column(String(2000), nullable=False)
    comentario = Column(String(500))

Desarrollo_Encuesta = Table('desarrollo_encuesta',db.Model.metadata,
    Column('id_encuesta',ForeignKey('encuesta.id_encuesta'), primary_key=True),
    Column('id_pregunta_desarrollo',ForeignKey('pregunta_desarrollo.id_pregunta_desarrollo'), primary_key=True)
)

class Pregunta_Alternativa(db.Model):
    __tablename__ = 'pregunta_alternativa'
    id_pregunta_alternativa = Column(Integer,primary_key=True,autoincrement=True)
    numero = Column(Integer)
    enunciado = Column(String(2000), nullable=False)
    comentario = Column(String(500))

Alternativa_Encuesta = Table('alternativa_encuesta',db.Model.metadata,
    Column('id_encuesta',ForeignKey('encuesta.id_encuesta'), primary_key=True),
    Column('id_pregunta_alternativa',ForeignKey('pregunta_alternativa.id_pregunta_alternativa'), primary_key=True)
)

class Opcion(db.Model):
    __tablename__ = 'opcion'
    id_opcion = Column(Integer,primary_key=True,autoincrement=True)
    opcion = Column(String(100))

Alternativas = Table('alternativas',db.Model.metadata,
    Column('id_pregunta_alternativa',ForeignKey('pregunta_alternativa.id_pregunta_alternativa'), primary_key=True),
    Column('id_opcion',ForeignKey('opcion.id_opcion'), primary_key=True)
)

class Encuestado(db.Model):
    __tablename__ = 'encuestado'
    id_encuestado = Column(Integer,primary_key=True,autoincrement=True)
    nombre = Column(String(100))
    email = Column(String(50), nullable=False)