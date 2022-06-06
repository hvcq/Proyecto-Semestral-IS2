from .consultas import *


def crear_dataSurvey(id_encuesta):
    datos_encuesta_creada = obtener_encuesta_creada(id_encuesta)
    questions = []
    # Se generan ordenados id_pregunta, enunciado y comentario por numero
    cantidad_total_preguntas = len(datos_encuesta_creada["ids_preguntas_alternativas"])
    indexOp = 0
    for i in range(0,cantidad_total_preguntas):
        data = {
            "id": datos_encuesta_creada["ids_preguntas_alternativas"].pop(0),
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

    dataSurvey = {
        "id": id_encuesta,
        "title": db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first().titulo,
        "description": db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first().descripcion,
        "questions": questions
    }

    return dataSurvey
