"""Tablas de la base de datos"""
from sqlalchemy import Table, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from time import timezone
from . import db


class Admin(db.Model):
    __tablename__ = 'admin'
    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(108), nullable=False)


class Encuesta(db.Model):
    __tablename__ = 'encuesta'
    id_encuesta = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(3000), nullable=False)
    fecha_inicio = Column(Date(), nullable=False)
    fecha_fin = Column(Date())
    activa = Column(Boolean, nullable=False)
    visitas = Column(Integer)
    respuestas = Column(Integer)
    total_asignados = Column(Integer)
    asunto_mail = Column(String(100))
    mensaje_mail = Column(String(500))


Crea_Encuesta = Table('crea_encuesta', db.Model.metadata,
                      Column('id_admin', ForeignKey(
                          'admin.id_admin'), primary_key=True),
                      Column('id_encuesta', ForeignKey(
                          'encuesta.id_encuesta'), primary_key=True)
                      )


class Pregunta_Alternativa(db.Model):
    __tablename__ = 'pregunta_alternativa'
    id_pregunta_alternativa = Column(
        Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)
    enunciado = Column(String(2000), nullable=False)


Alternativa_Encuesta = Table('alternativa_encuesta', db.Model.metadata,
                             Column('id_encuesta', ForeignKey(
                                 'encuesta.id_encuesta'), primary_key=True),
                             Column('id_pregunta_alternativa', ForeignKey(
                                 'pregunta_alternativa.id_pregunta_alternativa'), primary_key=True)
                             )


class Opcion(db.Model):
    __tablename__ = 'opcion'
    id_opcion = Column(Integer, primary_key=True, autoincrement=True)
    opcion = Column(String(300))


Alternativas = Table('alternativas', db.Model.metadata,
                     Column('id_pregunta_alternativa', ForeignKey(
                         'pregunta_alternativa.id_pregunta_alternativa'), primary_key=True),
                     Column('id_opcion', ForeignKey(
                         'opcion.id_opcion'), primary_key=True)
                     )


class Encuestado(db.Model):
    __tablename__ = 'encuestado'
    email = Column(String(50), primary_key=True)
    activo = Column(Boolean, nullable=False)


Encuestar = Table('encuestar', db.Model.metadata,
                              Column('id_encuesta', ForeignKey(
                                  'encuesta.id_encuesta'), primary_key=True),
                              Column('email', ForeignKey(
                                  'encuestado.email'), primary_key=True),
                              Column('contestada', Boolean, nullable=False),
                              Column('fecha_envio', Date()),
                              Column('fecha_contestada', Date())
                              )

Respuesta_Alternativa = Table('respuesta_alternativa', db.Model.metadata,
                              Column('id_opcion', ForeignKey(
                                  'opcion.id_opcion'), primary_key=True),
                              Column('email', ForeignKey(
                                  'encuestado.email'), primary_key=True)
                              )


class Registrado(db.Model):
    __tablename__ = 'registrado'
    id_registrado = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), ForeignKey("encuestado.email"))
    password = Column(String(108), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    rut = Column(String(12), nullable=False)
    genero = Column(String(1))
    fecha_nacimiento = Column(Date())
    fecha_registro = Column(Date())
