import email
from .models import *
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import base64
from werkzeug.security import generate_password_hash, check_password_hash

def obtener_encuestas():
    """Consulta para obtener todas las encuestas de la bd"""
    lista_encuestas = []
    if db.session.query(Encuesta).first() == None:
        return lista_encuestas
    else:
        tuplas_de_encuestas = db.session.query(Encuesta).order_by(Encuesta.id_encuesta).all()
        for tupla_encuesta in tuplas_de_encuestas:
            datos_encuesta_aux = {}
            datos_encuesta_aux.clear()
            if tupla_encuesta.fecha_fin == None:
                datos_encuesta_aux = {
                    "id_survey": tupla_encuesta.id_encuesta,
                    "title": tupla_encuesta.titulo,
                    "description": tupla_encuesta.descripcion,
                    "start_date": tupla_encuesta.fecha_inicio.strftime("%d/%m/%Y"),
                    "end_date": "",
                    "active" : tupla_encuesta.activa,
                    "comentario": tupla_encuesta.comentario,
                    "visits": tupla_encuesta.visitas,
                    "answers": {"total":tupla_encuesta.total_asignados,"current_answers": tupla_encuesta.respuestas}
                }
            else:
                datos_encuesta_aux = {
                    "id_survey": tupla_encuesta.id_encuesta,
                    "title": tupla_encuesta.titulo,
                    "description": tupla_encuesta.descripcion,
                    "start_date": tupla_encuesta.fecha_inicio.strftime("%d/%m/%Y"),
                    "end_date": tupla_encuesta.fecha_fin,
                    "active" : tupla_encuesta.activa,
                    "comentario": tupla_encuesta.comentario,
                    "visits": tupla_encuesta.visitas,
                    "answers": {"total":tupla_encuesta.total_asignados,"current_answers": tupla_encuesta.respuestas}
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
                    "registration_date": tupla_registrado_aux.fecha_registro.strftime("%d/%m/%Y"),
                    "gender": tupla_registrado_aux.genero,
                    "state": tupla_encuestado.activo,
                    "rut": tupla_registrado_aux.rut
                }
            dataUsers.append(datos_encuestado_aux)
            i = i + 1
        return dataUsers

def obtener_cantidad_registrados_e_invitados():
    cantidad_invitados = db.session.query(Encuestado).count()
    cantidad_registrados = db.session.query(Registrado).count()
    dataChart = {
        "anonymous": cantidad_invitados,
        "registered": cantidad_registrados
    }
    return dataChart

def obtener_encuesta_creada(id_encuesta):
    """Consulta para obtener datos de las preguntas"""
    ids_preguntas_alternativas = []
    numeros_preguntas_alternativas = []
    enunciados_preguntas_alternativas = []
    comentarios_preguntas_alternativas = []
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
            comentarios_preguntas_alternativas.append(
                tupla_pregunta_alternativa.comentario)
        for id_pregunta_alternativa in ids_preguntas_alternativas:
            if db.session.query(Alternativas).filter_by(id_pregunta_alternativa=id_pregunta_alternativa).first() != None:
                tuplas_alternativas_aux = db.session.query(Alternativas).filter_by(
                    id_pregunta_alternativa=id_pregunta_alternativa).all()
                k = 0
                for tupla_alternativa in tuplas_alternativas_aux:
                    ids_opciones.append(tupla_alternativa.id_opcion)
                    k = k + 1
                cantidad_opciones_por_pregunta.append(k)
        tuplas_opcion = db.session.query(Opcion).filter(
            Opcion.id_opcion.in_(ids_opciones)).all()
        for tupla_opcion in tuplas_opcion:
            strings_opciones.append(tupla_opcion.opcion)
        # id_opciones[i] y string_opciones[i] es una i-esima opcion

    """Se crea diccionario con las listas que contienen datos de la encuesta"""
    datos_encuesta_creada = {
        "ids_preguntas_alternativas": ids_preguntas_alternativas,
        "numeros_preguntas_alternativas": numeros_preguntas_alternativas,
        "enunciados_preguntas_alternativas": enunciados_preguntas_alternativas,
        "comentarios_preguntas_alternativas": comentarios_preguntas_alternativas,
        "cantidad_opciones_por_pregunta": cantidad_opciones_por_pregunta,
        "ids_opciones": ids_opciones,
        "strings_opciones": strings_opciones
    }
    return datos_encuesta_creada

def guardar_encuesta(surveyData,id_admin):
    if surveyData["title"] == "":
        encuesta_aux = Encuesta(titulo="titulo encuesta por defecto", descripcion=surveyData["description"],
            fecha_inicio=date.today(), activa=False, comentario="", visitas=0, respuestas=0, total_asignados=0)
    else:
        encuesta_aux = Encuesta(titulo=surveyData["title"], descripcion=surveyData["description"],
            fecha_inicio=date.today(), activa=False, comentario="", visitas=0, respuestas=0, total_asignados=0)
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
    print(surveyData)
    return("Modificacion Exitosa")
    # Modifica titulo y descripcion de la encuesta
    nueva_encuesta = db.session.query(Encuesta).filter_by(id_encuesta=surveyData["id"]).first()
    if surveyData["title"] == "":
        nueva_encuesta.titulo = "titulo encuesta por defecto"
    else:
        nueva_encuesta.titulo = surveyData["title"]
    nueva_encuesta.descripcion = surveyData["description"]
    db.session.commit()
    i = 1
    # Modifica las preguntas de la encuesta
    for pregunta in surveyData["questions"]:
        if db.session.query(Pregunta_Alternativa).filter_by(id_pregunta_alternativa=pregunta["id"]).first() != None:
            pregunta_alternativa_aux = db.session.query(Pregunta_Alternativa).filter_by(id_pregunta_alternativa=pregunta["id"]).first()
            pregunta_alternativa_aux.numero = i
            pregunta_alternativa_aux.enunciado = pregunta["statement"]
            db.session.commit()
            # Modifica las alternativas de una pregunta de alternativas
            for alternativa in pregunta["alternatives"]:
                # si existe, modifica dicha opcion, sino, la agrega
                if db.session.query(Opcion).filter_by(id_opcion=alternativa["id"]).first() != None:
                    opcion_aux = db.session.query(Opcion).filter_by(id_opcion=alternativa["id"]).first()
                    opcion_aux.opcion = alternativa["textAlt"]
                    db.session.commit()
                else:
                    opcion_aux = Opcion(opcion=alternativa["textAlt"])
                    db.session.add(opcion_aux)
                    db.session.commit()
                    alternativas_aux = Alternativas.insert().values(
                        id_pregunta_alternativa=pregunta["id"], id_opcion=opcion_aux.id_opcion)
                    db.engine.execute(alternativas_aux)
                    db.session.commit()
            # else, cuando se implemente borrar pregunta de alternativas
        i = i + 1
        # Aqui se aplican operaciones de borrado de preguntas
        # y opciones de una pregunta de alternativas
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
    # cuando se empiece a usar tabla crea_encuesta se debe borrar 
    # la tupla de esa tabla antes que la tupla de la tabla encuesta
    encuesta = db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first()
    db.session.delete(encuesta)
    db.session.commit()
    return "Borrada Correctamente"

def guardar_respuesta(responses):
    for i in range(0, len(responses["respuestas"])):
        respuesta_alternativa_aux = Respuesta_Alternativa.insert().values(
            id_opcion=responses["respuestas"][i]["response"]["idOpcion"], email=responses["correo"])
        db.engine.execute(respuesta_alternativa_aux)
        db.session.commit()
    return "Respuestas Guardada"

def obtener_numero_encuestados_activos():
    record = db.session.query(Encuestado).filter_by(activo=True).all()
    return (len(record))

#Se asume que no se pueden dejar encuestas incompletas
def obtener_numero_encuestados_responden(id_encuesta):

    preguntas_alternativas = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta = id_encuesta).all()
    
    total_responden = 0

    if preguntas_alternativas == None:
        return total_responden

    for op in preguntas_alternativas:
        list_opciones = db.session.query(Alternativas).filter_by(id_pregunta_alternativa = op[1]).all()
    
        suma_respuestas = 0
        for r in list_opciones:
            list_marcas = db.session.query(Respuesta_Alternativa).filter_by(id_opcion = r[1]).all()
            suma_respuestas = suma_respuestas + len(list_marcas)
            
        if (suma_respuestas > total_responden):
            total_responden = suma_respuestas

    return total_responden

#Se obtiene el título y descripción de la encuesta
def obtener_titulo_encuesta(id_encuesta):
    record = db.session.query(Encuesta).filter_by(id_encuesta = id_encuesta).first()

    if (record != None):
        titulo_encuesta = {
            "titulo" : record.titulo,
            "descripcion" : record.descripcion
        }
    else:
        titulo_encuesta = {
            "titulo" : None,
            "descripcion" : None,
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
                "comentario": None,
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
                "comentario": p.comentario,
                "opciones": lista_opciones
            }

            lista_preguntas.append(datos_pregunta)

    sorted(lista_preguntas, key = lambda i: i['numero'])

    return lista_preguntas

#Se obtienen los datos de los usuarios que responden la encuesta
#Se asume que no se pueden dejar encuestas incompletas
def obtener_encuestados_responden(id_encuesta):

    # Se obtienen la primera pregunta de alternativa de la encuestas
    primera_pregunta_alternativa = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta = id_encuesta).first()

    if primera_pregunta_alternativa == None:
        return None

    list_responden = []

    # Se obtienen las opciones de la primera pregunta
    list_opciones = db.session.query(Alternativas).filter_by(id_pregunta_alternativa = primera_pregunta_alternativa[1]).all()

    if list_opciones == None:
        return None

    #Por cada opcion se obtienen los emails de los encuestados
    for r in list_opciones:
        list_marcas = db.session.query(Respuesta_Alternativa).filter_by(id_opcion = r[1]).all()

        for l in list_marcas:
            if l != None:
                list_responden.append(l.email)

    if list_responden == None:
        return None

    list_encuestados = []

    #Se obtienen los datos de los encuestados:
    for i in list_responden:

        datos_encuestado = {}
        datos_encuestado.clear()

        encuestado = db.session.query(Registrado).filter_by(email=i).first()
        
        if(encuestado == None):
            datos_encuestado={
                "id_registrado": None,
                "email": i,
                "nombre": "Invitado",
                "apellido": "-", 
                "genero": "-",
                "edad": "-"
            }

        else:
            datos_encuestado={
                "id_registrado": encuestado.id_registrado,
                "email": i,
                "nombre": encuestado.nombre,
                "apellido": encuestado.apellidos,
                "genero": encuestado.genero,
                "edad": calcular_edad(encuestado.fecha_nacimiento)
            }
        
        list_encuestados.append(datos_encuestado)

    return (list_encuestados)

def calcular_edad(fecha_nacimiento):
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
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
#True: Ya la ha contestado
#Se asume que la encuesta es correcta, con al menos una pregunta y dos alternativas
def comprobar_encuestado_encuesta(id_encuesta, email):

    # Se obtienen la primera pregunta de alternativa
    primera_pregunta_alternativa = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta = id_encuesta).first()

     # Se obtienen las opciones de la primera pregunta
    list_opciones = db.session.query(Alternativas).filter_by(id_pregunta_alternativa = primera_pregunta_alternativa[1]).all()

    #Por cada opcion se obtienen los emails de los encuestados
    for op in list_opciones:
        
        #Lista de mails de encuestados
        list_mails = db.session.query(Respuesta_Alternativa).filter_by(id_opcion = op[1]).all()

        print("LIST MAILS")
        print(list_mails)

        #Si no hay respuestas de encuestados se cambia a la siguiente opcion
        if list_mails == None:
            continue
        
        #Si existe el mail en la lista
        # if email in list_mails:
        #     return True

        # #Se recorre la lista comprobando los mails
        for i in list_mails:

            #Si se encuentra el mail se retorna True
            if i[1] == email:
                return True

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

    if(dataRegister.get("genero") == 1):
        genero = "M"
    elif(dataRegister.get("genero") == 2):
        genero = "F"
    else:
        genero = "O"

    registrado = Registrado(email = dataRegister.get("email"), password = password, 
        nombre = dataRegister.get("name"), apellidos = dataRegister.get("apellido"),
        rut = dataRegister.get("rut"), genero = genero, fecha_nacimiento = dataRegister.get("fecha_nacimiento"),
        fecha_registro =  date.today() )

    db.session.add(registrado)
    db.session.commit()

    return "Registro Exitoso"
