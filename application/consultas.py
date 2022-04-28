from .models import *

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
        "ids_preguntas_desarrollo" : ids_preguntas_desarrollo,
        "numeros_preguntas_desarrollo" : numeros_preguntas_desarrollo,
        "enunciados_preguntas_desarrollo" : enunciados_preguntas_desarrollo,
        "comentarios_preguntas_desarrollo" : comentarios_preguntas_desarrollo,
        "ids_preguntas_alternativas" : ids_preguntas_alternativas,
        "numeros_preguntas_alternativas" : numeros_preguntas_alternativas,
        "enunciados_preguntas_alternativas" : enunciados_preguntas_alternativas,
        "comentarios_preguntas_alternativas" : comentarios_preguntas_alternativas,
        "cantidad_opciones_por_pregunta" : cantidad_opciones_por_pregunta,
        "ids_opciones" : ids_opciones,
        "strings_opciones" : strings_opciones
    }
    return datos_encuesta_creada