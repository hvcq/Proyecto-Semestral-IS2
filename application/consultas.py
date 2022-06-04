import email
from .models import *
from datetime import datetime, date

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
                    "start_date": tupla_encuesta.fecha_inicio,
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
                    "start_date": tupla_encuesta.fecha_inicio,
                    "end_date": tupla_encuesta.fecha_fin,
                    "active" : tupla_encuesta.activa,
                    "comentario": tupla_encuesta.comentario,
                    "visits": tupla_encuesta.visitas,
                    "answers": {"total":tupla_encuesta.total_asignados,"current_answers": tupla_encuesta.respuestas}
                }
            lista_encuestas.append(datos_encuesta_aux)
        return lista_encuestas

def obtener_encuesta_creada(id_encuesta):
    """Consulta para obtener datos de preguntas de desarrollo"""
    ids_preguntas_desarrollo = []
    numeros_preguntas_desarrollo = []
    enunciados_preguntas_desarrollo = []
    comentarios_preguntas_desarrollo = []
    if db.session.query(Desarrollo_Encuesta).filter_by(id_encuesta=id_encuesta).first() != None:
        tuplas_desarrollo_encuesta = db.session.query(
            Desarrollo_Encuesta).filter_by(id_encuesta=id_encuesta).all()
        for tupla_desarrollo_encuesta in tuplas_desarrollo_encuesta:
            ids_preguntas_desarrollo.append(
                tupla_desarrollo_encuesta.id_pregunta_desarrollo)
        tuplas_pregunta_desarrollo = db.session.query(Pregunta_Desarrollo).filter(
            Pregunta_Desarrollo.id_pregunta_desarrollo.in_(ids_preguntas_desarrollo)).order_by(Pregunta_Desarrollo.numero).all()
        ids_preguntas_desarrollo.clear()
        for tupla_pregunta_desarrollo in tuplas_pregunta_desarrollo:
            ids_preguntas_desarrollo.append(tupla_pregunta_desarrollo.id_pregunta_desarrollo)
            numeros_preguntas_desarrollo.append(
                tupla_pregunta_desarrollo.numero)
            enunciados_preguntas_desarrollo.append(
                tupla_pregunta_desarrollo.enunciado)
            comentarios_preguntas_desarrollo.append(
                tupla_pregunta_desarrollo.comentario)

    """Consulta para obtener datos de preguntas de alternativas"""
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
        "ids_preguntas_desarrollo": ids_preguntas_desarrollo,
        "numeros_preguntas_desarrollo": numeros_preguntas_desarrollo,
        "enunciados_preguntas_desarrollo": enunciados_preguntas_desarrollo,
        "comentarios_preguntas_desarrollo": comentarios_preguntas_desarrollo,
        "ids_preguntas_alternativas": ids_preguntas_alternativas,
        "numeros_preguntas_alternativas": numeros_preguntas_alternativas,
        "enunciados_preguntas_alternativas": enunciados_preguntas_alternativas,
        "comentarios_preguntas_alternativas": comentarios_preguntas_alternativas,
        "cantidad_opciones_por_pregunta": cantidad_opciones_por_pregunta,
        "ids_opciones": ids_opciones,
        "strings_opciones": strings_opciones
    }
    return datos_encuesta_creada

def guardar_encuesta(surveyData):
    if surveyData["title"] == "":
        encuesta_aux = Encuesta(titulo="titulo encuesta por defecto", descripcion=surveyData["description"],
            fecha_inicio=date.today(), activa=False, comentario="", visitas=0, respuestas=0, total_asignados=0)
    else:
        encuesta_aux = Encuesta(titulo=surveyData["title"], descripcion=surveyData["description"],
            fecha_inicio=date.today(), activa=False, comentario="", visitas=0, respuestas=0, total_asignados=0)
    db.session.add(encuesta_aux)
    db.session.commit()
    i = 1
    for pregunta in surveyData["questions"]:
        if pregunta["type"] == "desarrollo":
            pregunta_desarrollo_aux = Pregunta_Desarrollo(
                enunciado=pregunta["statement"], numero=i)
            db.session.add(pregunta_desarrollo_aux)
            db.session.commit()
            desarrollo_encuesta_aux = Desarrollo_Encuesta.insert().values(id_encuesta=encuesta_aux.id_encuesta,
                                                                          id_pregunta_desarrollo=pregunta_desarrollo_aux.id_pregunta_desarrollo)
            db.engine.execute(desarrollo_encuesta_aux)
            db.session.commit()
        else:
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
        if pregunta["type"] == "desarrollo":
            # si existe, modifica una pregunta de desarrollo
            if db.session.query(Pregunta_Desarrollo).filter_by(id_pregunta_desarrollo=pregunta["id"]).first() != None:
                pregunta_desarrollo_aux = db.session.query(Pregunta_Desarrollo).filter_by(id_pregunta_desarrollo=pregunta["id"]).first()
                pregunta_desarrollo_aux.numero = i
                pregunta_desarrollo_aux.enunciado = pregunta["statement"]
                db.session.commit()
            # else, cuando se implemente borrar pregunta de desarrollo
        else:
            # si existe, modifica una pregunta de alternativas
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
    ids_preguntas_desarrollo = []
    if db.session.query(Desarrollo_Encuesta).filter_by(id_encuesta=id_encuesta).first() != None:
        tuplas_desarrollo_encuesta = db.session.query(
            Desarrollo_Encuesta).filter_by(id_encuesta=id_encuesta).all()
        for tupla_desarrollo_encuesta in tuplas_desarrollo_encuesta:
            ids_preguntas_desarrollo.append(
                tupla_desarrollo_encuesta.id_pregunta_desarrollo)
        borra_tuplas_desarrollo_encuesta = Desarrollo_Encuesta.delete().where(Desarrollo_Encuesta.c.id_encuesta == id_encuesta)
        db.engine.execute(borra_tuplas_desarrollo_encuesta)
        db.session.commit()
        tuplas_pregunta_desarrollo = db.session.query(Pregunta_Desarrollo).filter(
            Pregunta_Desarrollo.id_pregunta_desarrollo.in_(ids_preguntas_desarrollo)).all()
        for tupla_pregunta_desarrollo in tuplas_pregunta_desarrollo:
            db.session.delete(tupla_pregunta_desarrollo)
            db.session.commit()
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
    encuestado_aux = Encuestado(
        email=responses["usuario"]["correo"],activo=True)
    db.session.add(encuestado_aux)
    db.session.commit()
    for i in range(0, len(responses["respuestas"])):
        if responses["respuestas"][i]["type"] == "desarrollo":
            respuesta_desarrollo_aux = Respuesta_Desarrollo.insert().values(
                id_pregunta_desarrollo=responses["respuestas"][i]["idPregunta"], email=encuestado_aux.email, respuesta_encuestado=responses["respuestas"][i]["response"])
            db.engine.execute(respuesta_desarrollo_aux)
            db.session.commit()
        else:
            respuesta_alternativa_aux = Respuesta_Alternativa.insert().values(
                id_opcion=responses["respuestas"][i]["response"]["idOpcion"], email=encuestado_aux.email)
            db.engine.execute(respuesta_alternativa_aux)
            db.session.commit()

    return "Respuesta Guardada"

def obtener_numero_encuestados_activos():
    record = db.session.query(Encuestado).filter_by(activo=True).all()
    return (len(record))

#Se asume que no se pueden dejar encuestas incompletas
def obtener_numero_encuestados_responden(id_encuesta):

    preguntas_alternativas = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta = id_encuesta).all()
    
    total_responden = 0

    for op in preguntas_alternativas:
        list_opciones = db.session.query(Alternativas).filter_by(id_pregunta_alternativa = op[1]).all()
        #print(list_opciones)
        suma_respuestas = 0
        for r in list_opciones:
            list_marcas = db.session.query(Respuesta_Alternativa).filter_by(id_opcion = r[1]).all()
            suma_respuestas = suma_respuestas + len(list_marcas)
            
        if (suma_respuestas > total_responden):
            total_responden = suma_respuestas

    return total_responden

#Se obtienen las respuestas de cada pregunta con la cantidad por cada opción
def obtener_respuestas_opcion(id_encuesta):
    
    record = db.session.query(Alternativa_Encuesta).filter_by(id_encuesta = id_encuesta).all()

    lista_preguntas = []

    for rec in record:
        # dato_pregunta = {}
        # dato_pregunta.clear()

        #print (rec[1])

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
                    "respuestas": numero_respuestas
                }

                lista_opciones.append(resultado_opcion)
            
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

    list_responden = []

    # for op in preguntas_alternativas:

    # Se obtienen las opciones de la primera pregunta
    list_opciones = db.session.query(Alternativas).filter_by(id_pregunta_alternativa = primera_pregunta_alternativa[1]).all()

    #Por cada opcion se obtienen los emails de los encuestados
    for r in list_opciones:
        list_marcas = db.session.query(Respuesta_Alternativa).filter_by(id_opcion = r[1]).all()

        for l in list_marcas:
            if l != None:
                list_responden.append(l.email)

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
                "nombre": "Anónimo",
                "genero": "-",
                "edad": "-"
            }

        else:
            datos_encuestado={
                "id_registrado": encuestado.id_registrado,
                "email": i,
                "nombre": encuestado.nombre,
                "genero": encuestado.genero,
                "edad": calcular_edad(encuestado.fecha_nacimiento)
            }
        
        list_encuestados.append(datos_encuestado)

    return (list_encuestados)


def calcular_edad(fecha_nacimiento):
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def agregar_usuario_anonimo():
    
    print()
