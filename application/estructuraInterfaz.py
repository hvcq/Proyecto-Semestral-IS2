from .consultas import *

def crear_dataSurvey(id_encuesta): 
    datos_encuesta_creada = obtener_encuesta_creada(id_encuesta)
    questions = []
    # Primero almacenaremos las preguntas de desarrollo.
    tam = len(datos_encuesta_creada["ids_preguntas_desarrollo"])
    i = 0
    while i < tam:
        data = {
            "id": datos_encuesta_creada["ids_preguntas_desarrollo"][i],
            "type": "desarrollo",
            "statement": datos_encuesta_creada["enunciados_preguntas_desarrollo"][i],
            "alternatives": []
        }
        questions.append(data)
        i += 1

    # Segundo almacenaremos las preguntas de desarrollo.
    tam = len(datos_encuesta_creada["ids_preguntas_alternativas"])
    i = 0
    indexOp = 0
    while i < tam:
        data = {
            "id": datos_encuesta_creada["ids_preguntas_alternativas"][i],
            "type": "alternativa",
            "statement": datos_encuesta_creada["enunciados_preguntas_alternativas"][i],
            "alternatives": []
        }
        tamAlt = datos_encuesta_creada["cantidad_opciones_por_pregunta"][i]
        j = 0
        while j < tamAlt:
            dataOption = {
                "id": datos_encuesta_creada["ids_opciones"][indexOp],
                "textAlt": datos_encuesta_creada["strings_opciones"][indexOp]
            }
            data["alternatives"].append(dataOption)
            j += 1
            print(datos_encuesta_creada["strings_opciones"][indexOp])
            print(indexOp)
            indexOp += 1
        indexOp = j
        questions.append(data)
        i += 1

    dataSurvey = {
        "id": id_encuesta,
        "title": db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first().titulo,
        "description": db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first().descripcion,
        "questions": questions
    }

    return dataSurvey