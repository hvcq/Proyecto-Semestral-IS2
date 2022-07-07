from .consultas import *


def crear_dataSurvey(id_encuesta):
    datos_encuesta_creada = obtener_encuesta_creada(id_encuesta)
    questions = []
    # Se generan ordenados id_pregunta y enunciado por numero
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

    survey = db.session.query(Encuesta).filter_by(id_encuesta=id_encuesta).first()

    fecha_fin_aux = ""
    if survey.fecha_fin == None:
        fecha_fin_aux = (datetime.now() + timedelta(days=7)).strftime("%d-%m-%Y")
    else:
        fecha_fin_aux = survey.fecha_fin.strftime("%d-%m-%Y")
        
    dataSurvey = {
        "id": id_encuesta,
        "title": survey.titulo,
        "description": survey.descripcion,
        "questions": questions, 
        "end_date": fecha_fin_aux,
        "mail_subject": survey.asunto_mail,
        "mail_body": survey.mensaje_mail,
        "asigned" : survey.total_asignados
    }

    return dataSurvey
