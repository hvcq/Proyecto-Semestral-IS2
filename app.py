from flask import Flask, render_template

app = Flask(__name__)


@app.route("/createSurvey/")
@app.route("/createSurvey/<string:section>")
def index(section="preguntas"):
    return render_template("admin/create_survey.html", navOptions={
        "options": ["Preguntas", "Respuestas", "Configuración"],
        "selected": section
    }
    )
