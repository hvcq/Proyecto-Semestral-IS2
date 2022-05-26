from .models import *
from datetime import datetime, date


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
            Pregunta_Desarrollo.id_pregunta_desarrollo.in_(ids_preguntas_desarrollo)).all()
        for tupla_pregunta_desarrollo in tuplas_pregunta_desarrollo:
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
            Pregunta_Alternativa.id_pregunta_alternativa.in_(ids_preguntas_alternativas)).all()
        for tupla_pregunta_alternativa in tuplas_pregunta_alternativa:
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
    encuesta_aux = Encuesta(
        titulo=surveyData["title"], descripcion=surveyData["description"], fecha_inicio=date.today(), activa=True)
    db.session.add(encuesta_aux)
    db.session.commit()
    for i in range(0, len(surveyData["questions"])):
        if surveyData["questions"][i]["type"] == "desarrollo":
            pregunta_desarrollo_aux = Pregunta_Desarrollo(
                enunciado=surveyData["questions"][i]["statement"])
            db.session.add(pregunta_desarrollo_aux)
            db.session.commit()
            desarrollo_encuesta_aux = Desarrollo_Encuesta.insert().values(id_encuesta=encuesta_aux.id_encuesta,
                                                                          id_pregunta_desarrollo=pregunta_desarrollo_aux.id_pregunta_desarrollo)
            db.engine.execute(desarrollo_encuesta_aux)
            db.session.commit()
        else:
            pregunta_alternativa_aux = Pregunta_Alternativa(
                enunciado=surveyData["questions"][i]["statement"])
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
