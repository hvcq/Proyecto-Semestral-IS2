import email
from flask_login import current_user
from .models import *
from datetime import datetime, date, timedelta 
from dateutil.relativedelta import relativedelta
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response, redirect, render_template, request, url_for

def obtener_encuestas():
    """Consulta para obtener todas las encuestas de la bd"""
    lista_encuestas = []
    if db.session.query(Encuesta).first() == None:
        return lista_encuestas
    else:
        tuplas_de_encuestas = db.session.query(Encuesta).order_by(Encuesta.id_encuesta).all()
        print(tuplas_de_encuestas)
        for tupla_encuesta in tuplas_de_encuestas:
            crea_encuesta_aux = db.session.query(Crea_Encuesta).filter_by(id_encuesta=tupla_encuesta.id_encuesta).first()
            admin_aux = db.session.query(Admin).filter_by(id_admin=crea_encuesta_aux.id_admin).first()
            datos_encuesta_aux = {}
            datos_encuesta_aux.clear()
            if tupla_encuesta.fecha_fin == None:
                datos_encuesta_aux = {
                    "id_survey": tupla_encuesta.id_encuesta,
                    "title": tupla_encuesta.titulo,
                    "description": tupla_encuesta.descripcion,
                    "start_date": tupla_encuesta.fecha_inicio.strftime("%d-%m-%Y"),
                    "end_date": "",
                    "active" : tupla_encuesta.activa,
                    "visits": tupla_encuesta.visitas,
                    "answers": {"total":tupla_encuesta.total_asignados,"current_answers": tupla_encuesta.respuestas},
                    "author": admin_aux.nombre,
                    "asigned" : tupla_encuesta.total_asignados
                }
            else:
                datos_encuesta_aux = {
                    "id_survey": tupla_encuesta.id_encuesta,
                    "title": tupla_encuesta.titulo,
                    "description": tupla_encuesta.descripcion,
                    "start_date": tupla_encuesta.fecha_inicio.strftime("%d-%m-%Y"),
                    "end_date": tupla_encuesta.fecha_fin,
                    "active" : tupla_encuesta.activa,
                    "visits": tupla_encuesta.visitas,
                    "answers": {"total":tupla_encuesta.total_asignados,"current_answers": tupla_encuesta.respuestas},
                    "author": admin_aux.nombre,
                    "asigned" : tupla_encuesta.total_asignados
                }
            lista_encuestas.append(datos_encuesta_aux)
        return lista_encuestas

def obtener_usuarios():
    """Consulta para obtener todos los usuarios encuestados (invitados y registrados)"""
    dataUsers = []
    if db.session.query(Encuestado).first() == None:
        return dataUsers
    else:
        tuplas_encuestados = db.session.query(Encuestado).order_by(Encuestado.email).all()
        i = 0
        for tupla_encuestado in tuplas_encuestados:
            datos_encuestado_aux = {}
            datos_encuestado_aux.clear()
            if db.session.query(Registrado).filter_by(email=tupla_encuestado.email).first() == None:
                datos_encuestado_aux = {
                    "id_user": i,
                    "name": "Invitado",
                    "lastName": "None",
                    "email": tupla_encuestado.email,
                    "age": "None",
                    "registration_date": None,
                    "gender": None,
                    "state": tupla_encuestado.activo,
                    "rut": "xx.xxx.xxx-x"
                }
            else:
                tupla_registrado_aux = db.session.query(Registrado).filter_by(email=tupla_encuestado.email).first()
                datos_encuestado_aux = {
                    "id_user": i,
                    "name": tupla_registrado_aux.nombre,
                    "lastName": tupla_registrado_aux.apellidos,
                    "email": tupla_encuestado.email,
                    "age": relativedelta(datetime.now(),datetime.combine(tupla_registrado_aux.fecha_nacimiento, datetime.min.time())).years,
                    "registration_date": tupla_registrado_aux.fecha_registro.strftime("%d-%m-%Y"),
                    "gender": tupla_registrado_aux.genero,
                    "state": tupla_encuestado.activo,
                    "rut": tupla_registrado_aux.rut
                }
            dataUsers.append(datos_encuestado_aux)
            i = i + 1
        return dataUsers

def obtener_cantidad_registrados_e_invitados():
    cantidad_registrados = db.session.query(Registrado).count()
    cantidad_invitados = db.session.query(Encuestado).count()
    dataChart = {
        "anonymous": cantidad_invitados - cantidad_registrados,
        "registered": cantidad_registrados
    }
    return dataChart

def obtener_encuesta_creada(id_encuesta):
    """Consulta para obtener datos de las preguntas"""
    ids_preguntas_alternativas = []
    numeros_preguntas_alternativas = []
    enunciados_preguntas_alternativas = []
    cantidad_opciones_por_pregunta = []
    ids_opciones = []
    strings_opciones = []
    if db.session.query(Alternativa_Encuesta).filter_by(id_encuesta=id_encuesta).first() != None:
        tuplas_alternativa_encuesta = db.session.query(
            Alternativa_Encuesta).filter_by(id_encuesta=id_encuesta).all()
        for tupla_alternativa_encuesta in tuplas_alternativa_encuesta:
            ids_preguntas_alternativas.append(
                tupla_alternativa_encuesta.id_pregunta_alternativa)
        tuplas_pregunta_alternativa = db.session.query(Pregunta_Alternativa).filter(
            Pregunta_Alternativa.id_pregunta_alternativa.in_(ids_preguntas_alternativas)).order_by(Pregunta_Alternativa.numero).all()
        ids_preguntas_alternativas.clear()
        for tupla_pregunta_alternativa in tuplas_pregunta_alternativa:
            ids_preguntas_alternativas.append(tupla_pregunta_alternativa.id_pregunta_alternativa)
            numeros_preguntas_alternativas.append(
                tupla_pregunta_alternativa.numero)
            enunciados_preguntas_alternativas.append(
                tupla_pregunta_alternativa.enunciado)
        for id_pregunta_alternativa in ids_preguntas_alternativas:
            if db.session.query(Alternativas).filter_by(id_pregunta_alternativa=id_pregunta_alternativa).first() != None:
                tuplas_alternativas_aux = db.session.query(Alternativas).filter_by(
                    id_pregunta_alternativa=id_pregunta_alternativa).all()
                k = 0
                for tupla_alternativa in tuplas_alternativas_aux:
                    ids_opciones.append(tupla_alternativa.id_opcion)
                    tupla_opcion_aux = db.session.query(Opcion).filter_by(id_opcion=tupla_alternativa.id_opcion).first()
                    strings_opciones.append(tupla_opcion_aux.opcion)
                    k = k + 1
                cantidad_opciones_por_pregunta.append(k)
        # id_opciones[i] y string_opciones[i] es una i-esima opcion

    """Se crea diccionario con las listas que contienen datos de la encuesta"""
    datos_encuesta_creada = {
        "ids_preguntas_alternativas": ids_preguntas_alternativas,
        "numeros_preguntas_alternativas": numeros_preguntas_alternativas,
        "enunciados_preguntas_alternativas": enunciados_preguntas_alternativas,
        "cantidad_opciones_por_pregunta": cantidad_opciones_por_pregunta,
        "ids_opciones": ids_opciones,
        "strings_opciones": strings_opciones
    }
    return datos_encuesta_creada

def guardar_encuesta(surveyData,id_admin):
    if surveyData["title"] == "":
        encuesta_aux = Encuesta(titulo="titulo encuesta por defecto", descripcion=surveyData["description"],
            fecha_inicio=date.today(), activa=False, visitas=0, respuestas=0, total_asignados=0, asunto_mail="", mensaje_mail="")
    else:
        encuesta_aux = Encuesta(titulo=surveyData["title"], descripcion=surveyData["description"],
            fecha_inicio=date.today(), activa=False, visitas=0, respuestas=0, total_asignados=0, asunto_mail="", mensaje_mail="")
    db.session.add(encuesta_aux)
    db.session.commit()
    crea_encuesta_aux = Crea_Encuesta.insert().values(
            id_admin=id_admin, id_encuesta=encuesta_aux.id_encuesta)
    db.engine.execute(crea_encuesta_aux)
    db.session.commit()
    i = 1
    for pregunta in surveyData["questions"]:
        pregunta_alternativa_aux = Pregunta_Alternativa(
            enunciado=pregunta["statement"], numero=i)
        db.session.add(pregunta_alternativa_aux)
        db.session.commit()
        alternativa_encuesta_aux = Alternativa_Encuesta.insert().values(
            id_encuesta=encuesta_aux.id_encuesta, id_pregunta_alternativa=pregunta_alternativa_aux.id_pregunta_alternativa)
        db.engine.execute(alternativa_encuesta_aux)
        db.session.commit()
        for alternativa in pregunta["alternatives"]:
            opcion_aux = Opcion(opcion=alternativa["textAlt"])
            db.session.add(opcion_aux)
            db.session.commit()
            alternativas_aux = Alternativas.insert().values(
                id_pregunta_alternativa=pregunta_alternativa_aux.id_pregunta_alternativa, id_opcion=opcion_aux.id_opcion)
            db.engine.execute(alternativas_aux)
            db.session.commit()
        i = i + 1
    return "Encuesta Guardada"

def modificar_encuesta(surveyData):

    # Modifica titulo y descripcion de la encuesta
    nueva_encuesta = db.session.query(Encuesta).filter_by(id_encuesta=surveyData["id"]).first()
    if surveyData["title"] == "":
        nueva_encuesta.titulo = "titulo encuesta por defecto"
    else:
        nueva_encuesta.titulo = surveyData["title"]
    nueva_encuesta.descripcion = surveyData["description"]
    db.session.commit()

    # Elimina las preguntas de la encuesta que se quitaron en la interfaz
    ids_preguntas_a_borrar = []
    ids_preguntas_surveyData = []
    for pregunta in surveyData["questions"]:
        ids_preguntas_surveyData.append(pregunta["id"])

    if db.session.query(Alternativa_Encuesta).filter_by(id_encuesta=surveyData["id"]).first() != None:
        tuplas_alternativa_encuesta = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta=surveyData["id"]).all()
        for tupla_alternativa_encuesta in tuplas_alternativa_encuesta:
            if tupla_alternativa_encuesta.id_pregunta_alternativa not in ids_preguntas_surveyData:
                borra_tupla_alternativa_encuesta = Alternativa_Encuesta.delete().where(Alternativa_Encuesta.c.id_pregunta_alternativa == tupla_alternativa_encuesta.id_pregunta_alternativa)
                db.engine.execute(borra_tupla_alternativa_encuesta)
                db.session.commit()
                ids_preguntas_a_borrar.append(tupla_alternativa_encuesta.id_pregunta_alternativa)

        ids_opciones_a_borrar = []
        for id_pregunta_a_borrar in ids_preguntas_a_borrar:
            if db.session.query(Alternativas).filter_by(id_pregunta_alternativa=id_pregunta_a_borrar).first() != None:
                tuplas_alternativas_aux = db.session.query(Alternativas).filter_by(
                    id_pregunta_alternativa=id_pregunta_a_borrar).all()
                for tupla_alternativa in tuplas_alternativas_aux:
                    ids_opciones_a_borrar.append(tupla_alternativa.id_opcion)
                borra_tuplas_alternativas = Alternativas.delete().where(Alternativas.c.id_pregunta_alternativa == id_pregunta_a_borrar)
                db.engine.execute(borra_tuplas_alternativas)
                db.session.commit()

        tuplas_opcion = db.session.query(Opcion).filter(Opcion.id_opcion.in_(ids_opciones_a_borrar)).all()
        for tupla_opcion in tuplas_opcion:
            db.session.delete(tupla_opcion)
            db.session.commit()

        tuplas_pregunta_alternativa = db.session.query(Pregunta_Alternativa).filter(
            Pregunta_Alternativa.id_pregunta_alternativa.in_(ids_preguntas_a_borrar)).all()
        for tupla_pregunta_alternativa in tuplas_pregunta_alternativa:
            db.session.delete(tupla_pregunta_alternativa)
            db.session.commit()

    # Crea lista de preguntas a modificar
    ids_preguntas_a_modificar = []
    if db.session.query(Alternativa_Encuesta).filter_by(id_encuesta=surveyData["id"]).first() != None:
        tuplas_alternativa_encuesta = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta=surveyData["id"]).all()
        for tupla_alternativa_encuesta in tuplas_alternativa_encuesta:
                ids_preguntas_a_modificar.append(tupla_alternativa_encuesta.id_pregunta_alternativa)

    i = 1
    for pregunta in surveyData["questions"]:
        # Modifica preguntas de acuerdo a la lista
        if pregunta["id"] in ids_preguntas_a_modificar:
            pregunta_alternativa_aux = db.session.query(Pregunta_Alternativa).filter_by(id_pregunta_alternativa=pregunta["id"]).first()
            pregunta_alternativa_aux.numero = i
            pregunta_alternativa_aux.enunciado = pregunta["statement"]
            db.session.commit()
            # Elimina las alternativas que ya no incluye la pregunta
            ids_opciones_surveyData = []
            ids_opciones_a_borrar2 = []

            for alternativa in pregunta["alternatives"]:
                ids_opciones_surveyData.append(alternativa["id"])
            
            tuplas_alternativas_aux = db.session.query(Alternativas).filter_by(
                id_pregunta_alternativa=pregunta["id"]).all()
            for tupla_alternativa in tuplas_alternativas_aux:
                if tupla_alternativa.id_opcion not in ids_opciones_surveyData:
                    ids_opciones_a_borrar2.append(tupla_alternativa.id_opcion)
                    borra_tupla_alternativas = Alternativas.delete().where(Alternativas.c.id_opcion == tupla_alternativa.id_opcion)
                    db.engine.execute(borra_tupla_alternativas)
                    db.session.commit()
            tuplas_opcion = db.session.query(Opcion).filter(Opcion.id_opcion.in_(ids_opciones_a_borrar2)).all()
           
            for tupla_opcion in tuplas_opcion:
                db.session.delete(tupla_opcion)
                db.session.commit()
            
            ids_opciones_a_borrar2.clear()

            # Crea lista de opciones a modificar
            ids_opciones_a_modificar = []
            if db.session.query(Alternativas).filter_by(id_pregunta_alternativa=pregunta["id"]).first() != None:
                tuplas_alternativas_aux = db.session.query(Alternativas).filter_by(
                    id_pregunta_alternativa=pregunta["id"]).all()
                for tupla_alternativa_aux in tuplas_alternativas_aux:
                    if tupla_alternativa_aux.id_opcion in ids_opciones_surveyData:
                        ids_opciones_a_modificar.append(tupla_alternativa_aux.id_opcion)
                
            for alternativa in pregunta["alternatives"]:
                # Modifica opciones de acuerdo a la lista
                if alternativa["id"] in ids_opciones_a_modificar:
                    opcion_aux = db.session.query(Opcion).filter_by(id_opcion=alternativa["id"]).first()
                    opcion_aux.opcion = alternativa["textAlt"]
                    db.session.commit()
                # Crea las opciones que no estaban en la lista
                else:
                    opcion_aux = Opcion(opcion=alternativa["textAlt"])
                    db.session.add(opcion_aux)
                    db.session.commit()
                    alternativas_aux = Alternativas.insert().values(
                        id_pregunta_alternativa=pregunta["id"], id_opcion=opcion_aux.id_opcion)
                    db.engine.execute(alternativas_aux)
                    db.session.commit()

            ids_opciones_a_modificar.clear()
            ids_opciones_surveyData.clear()
        # Crea las preguntas que no estaban en la lista
        else:
            pregunta_alternativa_aux = Pregunta_Alternativa(
                enunciado=pregunta["statement"], numero=i)
            db.session.add(pregunta_alternativa_aux)
            db.session.commit()

            alternativa_encuesta_aux = Alternativa_Encuesta.insert().values(
                id_encuesta=surveyData["id"], id_pregunta_alternativa=pregunta_alternativa_aux.id_pregunta_alternativa)
            db.engine.execute(alternativa_encuesta_aux)
            db.session.commit()
            for alternativa in pregunta["alternatives"]:
                opcion_aux = Opcion(opcion=alternativa["textAlt"])
                db.session.add(opcion_aux)
                db.session.commit()
                alternativas_aux = Alternativas.insert().values(
                    id_pregunta_alternativa=pregunta_alternativa_aux.id_pregunta_alternativa, id_opcion=opcion_aux.id_opcion)
                db.engine.execute(alternativas_aux)
                db.session.commit()
        i = i + 1

    return("Modificacion Exitosa")


def eliminar_encuesta(id_encuesta):
    ids_preguntas_alternativas = []
    if db.session.query(Alternativa_Encuesta).filter_by(id_encuesta=id_encuesta).first() != None:
        tuplas_alternativa_encuesta = db.session.query(
            Alternativa_Encuesta).filter_by(id_encuesta=id_encuesta).all()
        for tupla_alternativa_encuesta in tuplas_alternativa_encuesta:
            ids_preguntas_alternativas.append(
                tupla_alternativa_encuesta.id_pregunta_alternativa)
        borra_tuplas_alternativa_encuesta = Alternativa_Encuesta.delete().where(Alternativa_Encuesta.c.id_encuesta == id_encuesta)
        db.engine.execute(borra_tuplas_alternativa_encuesta)
        db.session.commit()
        ids_opciones = []
        for id_pregunta_alternativa in ids_preguntas_alternativas:
            if db.session.query(Alternativas).filter_by(id_pregunta_alternativa=id_pregunta_alternativa).first() != None:
                tuplas_alternativas_aux = db.session.query(Alternativas).filter_by(
                    id_pregunta_alternativa=id_pregunta_alternativa).all()
                for tupla_alternativa in tuplas_alternativas_aux:
                    ids_opciones.append(tupla_alternativa.id_opcion)
                borra_tuplas_alternativas = Alternativas.delete().where(Alternativas.c.id_pregunta_alternativa == id_pregunta_alternativa)
                db.engine.execute(borra_tuplas_alternativas)
                db.session.commit()
        tuplas_opcion = db.session.query(Opcion).filter(
            Opcion.id_opcion.in_(ids_opciones)).all()
        for tupla_opcion in tuplas_opcion:
            db.session.delete(tupla_opcion)
            db.session.commit()
        tuplas_pregunta_alternativa = db.session.query(Pregunta_Alternativa).filter(
            Pregunta_Alternativa.id_pregunta_alternativa.in_(ids_preguntas_alternativas)).all()
        for tupla_pregunta_alternativa in tuplas_pregunta_alternativa:
            db.session.delete(tupla_pregunta_alternativa)
            db.session.commit()
    # Elimina relacion encuesta-admin
    crea_encuesta = Crea_Encuesta.delete().where(Crea_Encuesta.c.id_encuesta == id_encuesta)
    db.engine.execute(crea_encuesta)
    db.session.commit()
    # Con la tupla que encuesta-admin eliminada, se puede borrar la tupla de encuesta
    encuesta = db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first()
    db.session.delete(encuesta)
    db.session.commit()
    return "Borrada Correctamente"

def guardar_respuesta(responses):
    # Incrementa la cantidad de respuestas de una encuesta
    encuesta_aux = db.session.query(Encuesta).filter_by(id_encuesta=responses["id"]).first()
    respuestas_actuales = encuesta_aux.respuestas
    encuesta_aux.respuestas = respuestas_actuales + 1
    db.session.commit()
    # Almacena en la base de datos las respuestas de un usuario
    for i in range(0, len(responses["respuestas"])):
        respuesta_alternativa_aux = Respuesta_Alternativa.insert().values(
            id_opcion=responses["respuestas"][i]["response"]["idOpcion"], email=responses["correo"])
        db.engine.execute(respuesta_alternativa_aux)
        db.session.commit()

    # Se guarda la fecha en donde el encuestado contesto la encuesta
    encuestar_aux = Encuestar.update().values(
        fecha_contestada=date.today(), contestada=True).where(Encuestar.c.email == responses["correo"])
    db.engine.execute(encuestar_aux)
    db.session.commit()
    return "Respuestas Guardada"

def obtener_numero_encuestados_activos():
    record = db.session.query(Encuestado).filter_by(activo=True).all()
    return (len(record))

def obtener_numero_encuestados_responden(id_encuesta):

    total_responden = db.session.query(Encuestar).filter_by(id_encuesta = id_encuesta, contestada = True).count()
    return total_responden

#Se obtiene el título de la encuesta
def obtener_titulo_encuesta(id_encuesta):
    record = db.session.query(Encuesta).filter_by(id_encuesta = id_encuesta).first()

    if (record != None):
        titulo_encuesta = {
            "titulo" : record.titulo
        }
    else:
        titulo_encuesta = {
            "titulo" : None
        }
    return (titulo_encuesta)

#Se obtienen las respuestas de cada pregunta con la cantidad por cada opción
def obtener_respuestas_opcion(id_encuesta):
    
    record = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta = id_encuesta).all()

    if record == None:

        datos_pregunta = {
                "id_pregunta": None,
                "numero": None,
                "enunciado": None,
                "opciones": []
            }
            
        return (datos_pregunta)

    lista_preguntas = []

    for rec in record:

        pregunta = db.session.query(Pregunta_Alternativa).filter_by(id_pregunta_alternativa = rec[1]).all()
        
        for p in pregunta:
            
            datos_pregunta = {}
            datos_pregunta.clear()            

            opciones = db.session.query(Alternativas).filter_by(id_pregunta_alternativa = p.id_pregunta_alternativa).all()

            lista_opciones = []

            for op in opciones:
                resultado_opcion = {}
                resultado_opcion.clear()
                respuestas = db.session.query(Respuesta_Alternativa).filter_by(id_opcion = op.id_opcion).all()
                numero_respuestas = len(respuestas)

                opcion = db.session.query(Opcion).filter_by(id_opcion = op.id_opcion).first()

                resultado_opcion = {
                    "id_opcion": op.id_opcion,
                    "opcion": opcion.opcion,
                    "respuestas": numero_respuestas,
                    "porcentaje": 0
                }

                lista_opciones.append(resultado_opcion)
            
            total_respuestas = 0
            for i in lista_opciones:
                total_respuestas = total_respuestas + i.get("respuestas")
            
            if (total_respuestas != 0):
                for i in lista_opciones:
                    i["porcentaje"] = round((i.get("respuestas")/total_respuestas)*100,1)
                
            datos_pregunta = {
                "id_pregunta":p.id_pregunta_alternativa,
                "numero": p.numero,
                "enunciado": p.enunciado,
                "opciones": lista_opciones,
                "total_respuestas": total_respuestas
            }

            lista_preguntas.append(datos_pregunta)

    sorted(lista_preguntas, key = lambda i: i['numero'])

    return lista_preguntas

#Se obtienen los datos de los usuarios que responden la encuesta
#Se asume que no se pueden dejar encuestas incompletas
def obtener_encuestados_responden(id_encuesta):

    responden = db.session.query(Encuestar).filter_by(id_encuesta = id_encuesta).all() 

    list_encuestados = []

    for i in responden:

        datos_encuestado = {}
        datos_encuestado.clear()

        if (i.contestada == True):
            estado = "Contestada"
        else:
            estado = "No Contestada"

        encuestado = db.session.query(Registrado).filter_by(email=i.email).first()

        if(encuestado == None):
            datos_encuestado={
                "id_registrado": None,
                "email": i.email,
                "nombre": "Invitado",
                "apellido": "-", 
                "genero": "-",
                "edad": "-",
                "estado": estado
            }

        else:
            datos_encuestado={
                "id_registrado": encuestado.id_registrado,
                "email": i.email,
                "nombre": encuestado.nombre,
                "apellido": encuestado.apellidos,
                "genero": encuestado.genero,
                "edad": calcular_edad(encuestado.fecha_nacimiento),
                "estado": estado
            }
        
        list_encuestados.append(datos_encuestado)

    return (list_encuestados)

def calcular_edad(fecha_nacimiento):
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    if(edad < 0):
        edad = 0
    return edad

def agregar_invitado(responses):
    encuestado_invitado = Encuestado(email=responses["email"],activo=False)
    db.session.add(encuestado_invitado)
    db.session.commit()
    return print("Usuario invitado se ha agregado correctamente")

def cambiar_estado_invitado(responses):
    encuestado_invitado = db.session.query(Encuestado).filter_by(email=responses["email"]).first()
    encuestado_invitado.activo = responses["state"]
    db.session.commit()
    return print("Estado de usuario invitado cambiado correctamente")

def desunscribir_registrado(response):
    if db.session.query(Registrado).filter_by(id_registrado=response["id_survey"]).first() != None:
        registrado_aux = db.session.query(Registrado).filter_by(id_registrado=response["id_survey"]).first()
        db.session.delete(registrado_aux)
        db.session.commit()
        return "USUARIO DESUSCRITO"
    else:
        return "Error: este usuario no esta registrado"

#Obtener el link personalizado desde el mail
def codificar_mail(mail):
    str_bytes = mail.encode("ascii")    
    base_bytes = base64.b64encode(str_bytes)
    return base_bytes.decode("ascii")

#Obtener el mail desde el link personalizado
def decodificar_mail(code):
    base_bytes = code.encode("ascii")
    str_bytes = base64.b64decode(base_bytes)
    return str_bytes.decode("ascii")

#Comprueba si el encuestado ha contestado la encuesta previamente
#También se comprueba si la fecha de la encuesta no ha finalizado
#True: Ya la ha contestado
def comprobar_encuestado_encuesta(id_encuesta, email):

    respondida = db.session.query(Encuestar).filter_by(id_encuesta=id_encuesta, email=email).first()

    #Si no se ha enviado por mail, no puede contestar
    if (respondida == None):
        return True

    if (respondida.contestada == True):
        return True

    else:
        #comprobación de la fecha
        encuesta = db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first()

        #Si la fecha_fin es menor a la fecha actual
        if(encuesta.fecha_fin != None and encuesta.fecha_fin < date.today()):
            encuesta.activa = False
            db.session.commit()

            return True
        
        else:
            return False

def cambiar_estado_encuesta(responses):

    encuesta = db.session.query(Encuesta).filter_by(id_encuesta = responses["id_survey"]).first()

    if encuesta != None:

        encuesta.activa = responses["status"]
        db.session.commit()
        
    return "Estado cambiado con exito!"

def comprobar_tipo_encuestado(email):

    encuestado = db.session.query(Registrado).filter_by(email = email).first()

    if(encuestado == None):
        return ("anonimo")
    
    else:
        return ("registrado")

def registrar_encuestado(dataRegister):

    if (db.session.query(Registrado).filter_by(email = dataRegister.get("email")).first() != None):
        return "Email ya registrado"
    
    if (db.session.query(Encuestado).filter_by(email = dataRegister.get("email")).first() == None):
        encuestado = Encuestado(email = dataRegister.get("email"), activo = True)
        db.session.add(encuestado)
        db.session.commit()

    password = generate_password_hash(dataRegister.get("password"))

    if(dataRegister.get("genero") == "1"):
        genero = "M"
    elif(dataRegister.get("genero") == "2"):
        genero = "F"
    else:
        genero = "O"

    registrado = Registrado(email = dataRegister.get("email"), password = password, 
        nombre = dataRegister.get("name"), apellidos = dataRegister.get("apellido"),
        rut = dataRegister.get("rut"), genero = genero, fecha_nacimiento = dataRegister.get("fecha_nacimiento"),
        fecha_registro =  date.today() )

    db.session.add(registrado)
    db.session.commit()

    return redirect(url_for("dashboard_user"))

def aumentar_visitas(id_encuesta):
    encuesta = db.session.query(Encuesta).filter_by(id_encuesta = id_encuesta).first()

    if (encuesta != None):

        encuesta.visitas = encuesta.visitas + 1
        db.session.commit()
    
    return "Visitas actualizadas"

def modificar_tiempo_limite(responses):
    from dateutil import parser
    encuesta = db.session.query(Encuesta).filter_by(id_encuesta = responses["id"]).first()
    if responses["end_date"] == "":
        return "error: Fecha de termino vacia"

    dt = parser.parse(responses["end_date"])
    fecha_termino = datetime.strftime(dt, '%Y-%m-%d')
    fecha_inicio = datetime.strftime(encuesta.fecha_inicio, '%Y-%m-%d')

    if fecha_inicio >= fecha_termino:
        return "error: Fecha de termino mayor o igual a la de inicio"
    encuesta.fecha_fin = responses["end_date"]
    db.session.commit()
    return "Tiempo limite de encuesta modificado correctamente"

def asignar_asunto_y_mensaje(responses):
    encuesta = db.session.query(Encuesta).filter_by(id_encuesta = responses["id"]).first()
    
    encuesta.asunto_mail = responses["mail_subject"]
    encuesta.mensaje_mail = responses["mail_body"]
    db.session.commit()

    return "Asunto y mensaje actualizados"

def desunscribir_encuestado(email):

    encuestado = db.session.query(Encuestado).filter_by(email = email).first()

    if(encuestado != None):
        encuestado.activo = False
        db.session.commit()

        return "Usuario desuscrito"

    else: 
        return "Email no existe"

def get_dataUser():
    dataUser = {}
    if current_user.rol == "admin":
        admin = db.session.query(Admin).filter_by(id_admin=current_user.id).first()
        dataUser = {
            "name": admin.nombre,
            "lastName": "None",
            "rut": "None",
            "gender": "None",
            "birthday": "dd-mm-aaaa",
            "email": admin.email,
            "avatar": "None",
            "encuestas": []
        }

    if current_user.rol == "encuestado":
        encuestado = db.session.query(Encuestado).filter_by(email=current_user.email).first()
        dataUser = {
            "name": "Invitado",
            "lastName": "None",
            "rut": "None",
            "gender": "None",
            "birthday": "dd-mm-aaaa",
            "email": encuestado.email,
            "avatar": "None",
            "encuestas": []
        }

    if current_user.rol == "registrado":
        registrado = db.session.query(Registrado).filter_by(id_registrado=current_user.id).first()
        encuestado = db.session.query(Encuestado).filter_by(email=current_user.email).first()
        genero = ""
        if registrado.genero == "M":
            genero = "Masculino"
        elif registrado.genero == "F":
            genero = "Femenino"
        else:
            genero = "No especificado"

        encuestas = db.session.query(Encuestar).filter_by(email=current_user.email, contestada=True).all()
        lista_encuestas = []

        if (encuestas != None):

            for l in encuestas:

                e = db.session.query(Encuesta).filter_by(id_encuesta = l.id_encuesta).first()
                encuesta={
                    "title": e.titulo,
                    "date": (l.fecha_contestada).strftime("%d-%m-%Y")
                }

                lista_encuestas.append(encuesta)
        

        dataUser = {
            "name": registrado.nombre,
            "lastName": registrado.apellidos,
            "rut": registrado.rut,
            "gender": genero,
            "birthday": registrado.fecha_nacimiento.strftime("%d-%m-%Y"),
            "email": registrado.email,
            "avatar": registrado.avatar,
            "estado": encuestado.activo,
            "encuestas": lista_encuestas
        }
    return dataUser

# Falta testing
def cambiar_password(user, password):

    usuario = db.session.query(Admin).filter_by(email=user).first()

    if (usuario == None):
        usuario = db.session.query(Registrado).filter_by(email=user).first()

        if(usuario == None):
            return "mail incorrecto"
        
    usuario.password = generate_password_hash(password)
    db.session.commit()

    return "password cambiada exitosamente"

# Cambia la imagen del avatar del usario
def cambiar_avatar(user, url):

    usuario = db.session.query(Admin).filter_by(email=user).first()

    if (usuario == None):
        usuario = db.session.query(Registrado).filter_by(email=user).first()

        if(usuario == None):
            return "usuario incorrecto"
        
    usuario.avatar = url
    db.session.commit()

    return "avatar cambiado correctamente"

