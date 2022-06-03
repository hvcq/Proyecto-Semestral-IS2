from .consultas import *


def crear_dataSurvey(id_encuesta):
    datos_encuesta_creada = obtener_encuesta_creada(id_encuesta)
    questions = []
    # Tenemos ordenados numero, enunciado y comentario por numero (numero de pregunta)
    # data.id representa el numero de pregunta
    cantidad_total_preguntas = len(datos_encuesta_creada["ids_preguntas_desarrollo"]) + len(datos_encuesta_creada["ids_preguntas_alternativas"])
    i = 0
    indexOp = 0
    while i < cantidad_total_preguntas:
        if len(datos_encuesta_creada["numeros_preguntas_desarrollo"]) > 0 and datos_encuesta_creada["numeros_preguntas_desarrollo"][0] == i+1:
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
            cantidad_alternativas = datos_encuesta_creada["cantidad_opciones_por_pregunta"].pop(0)
            j = 0
            while j < cantidad_alternativas:
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

# def crear_dataEncuestados(id_encuesta):

#     datos_encuestados = obtener_encuestados_responden(id_encuesta)

#     dataAnswer = {
        
#     }

    