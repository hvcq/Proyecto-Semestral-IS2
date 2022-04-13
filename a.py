from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/otros")
def otros():
    return "<h1> otros </h1>"

if __name__ == "__main__":
    app.run(debug=True)