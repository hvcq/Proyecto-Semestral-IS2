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
    encuesta_aux = Encuesta(titulo=surveyData["title"], descripcion=surveyData["description"],
        fecha_inicio=date.today(), activa=True, comentario="", visitas=0, respuestas=0, total_asignados=0)
    db.session.add(encuesta_aux)
    db.session.commit()
    for i in range(0, len(surveyData["questions"])):
        print(surveyData["questions"][i])
        if surveyData["questions"][i]["type"] == "desarrollo":
            pregunta_desarrollo_aux = Pregunta_Desarrollo(
                enunciado=surveyData["questions"][i]["statement"], numero=i+1)
            db.session.add(pregunta_desarrollo_aux)
            db.session.commit()
            desarrollo_encuesta_aux = Desarrollo_Encuesta.insert().values(id_encuesta=encuesta_aux.id_encuesta,
                                                                          id_pregunta_desarrollo=pregunta_desarrollo_aux.id_pregunta_desarrollo)
            db.engine.execute(desarrollo_encuesta_aux)
            db.session.commit()
        else:
            pregunta_alternativa_aux = Pregunta_Alternativa(
                enunciado=surveyData["questions"][i]["statement"], numero=i+1)
            db.session.add(pregunta_alternativa_aux)
            db.session.commit()
            alternativa_encuesta_aux = Alternativa_Encuesta.insert().values(
                id_encuesta=surveyData["id"], id_pregunta_alternativa=pregunta_alternativa_aux.id_pregunta_alternativa)
            db.engine.execute(alternativa_encuesta_aux)
            db.session.commit()
            for j in range(0, len(surveyData["questions"][i]["alternatives"])):
                opcion_aux = Opcion(
                    opcion=surveyData["questions"][i]["alternatives"][j]["textAlt"])
                db.session.add(opcion_aux)
                db.session.commit()
                alternativas_aux = Alternativas.insert().values(
                    id_pregunta_alternativa=pregunta_alternativa_aux.id_pregunta_alternativa, id_opcion=opcion_aux.id_opcion)
                db.engine.execute(alternativas_aux)
                db.session.commit()
    return "guardado"


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
    return "guardado"
