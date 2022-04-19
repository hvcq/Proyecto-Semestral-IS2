from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("admin/create_survey.html", navOptions={
        "options": ["Preguntas", "Respuestas", "Configuración"],
        "selected": "Preguntas"
    }
    )
