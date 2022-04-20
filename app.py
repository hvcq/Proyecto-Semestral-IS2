from flask import Flask, render_template

app = Flask(__name__)


@app.route("/createSurvey/<string:section>")
def index(section):
    return render_template("admin/create_survey.html", navOptions={
        "options": ["Preguntas", "Respuestas", "Configuración"],
        "selected": section
    }
    )
