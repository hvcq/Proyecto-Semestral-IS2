from .consultas import *


def crear_dataSurvey(id_encuesta):
    datos_encuesta_creada = obtener_encuesta_creada(id_encuesta)
    questions = []
    # Tenemos ordenados numero, enunciado y comentario por numero (numero de pregunta)
    # data.id representa el numero de pregunta
    tam = len(datos_encuesta_creada["ids_preguntas_desarrollo"]) + len(datos_encuesta_creada["ids_preguntas_alternativas"])
    i = 0
    indexOp = 0
    while i < tam:
        if datos_encuesta_creada["numeros_preguntas_desarrollo"][0] == i+1:
            data = {
                "id": datos_encuesta_creada["numeros_preguntas_desarrollo"].pop(0),
                "type": "desarrollo",
                "statement": datos_encuesta_creada["enunciados_preguntas_desarrollo"].pop(0),
                "alternatives": []
            }
            questions.append(data)
        else:
            data = {
                "id": datos_encuesta_creada["numeros_preguntas_alternativas"].pop(0),
                "type": "alternativa",
                "statement": datos_encuesta_creada["enunciados_preguntas_alternativas"].pop(0),
                "alternatives": []
            }
            tamAlt = datos_encuesta_creada["cantidad_opciones_por_pregunta"].pop(0)
            j = 0
            while j < tamAlt:
                dataOption = {
                    "id": datos_encuesta_creada["ids_opciones"][indexOp],
                    "textAlt": datos_encuesta_creada["strings_opciones"][indexOp]
                }
                data["alternatives"].append(dataOption)
                j += 1
                indexOp += 1
            questions.append(data)
        i += 1

    dataSurvey = {
        "id": id_encuesta,
        "title": db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first().titulo,
        "description": db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first().descripcion,
        "questions": questions
    }

    return dataSurvey
