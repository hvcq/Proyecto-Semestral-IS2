from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rnaqogegqudjaa:95f4d011f20c61f80d3a0def65691ecd433ffc2b6f82f3b79c34478338b3f426@ec2-34-192-210-139.compute-1.amazonaws.com:5432/d90hcs7h2r31b6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/guardar_nombre", methods=['POST'])
def guardar_nombre():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nombre_aux = Persona(id = 1, nombre = nombre)
        db.session.add(nombre_aux)
        db.session.commit()
        print(nombre)
        return 'received'
@app.route("/otros/")
def otros():
    return "<h1> otros </h1>"

if __name__ == "__main__":
    app.run(port = 3000, debug=True)