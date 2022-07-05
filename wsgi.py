"""Archivo ejecutable"""
from application import create_app
from flask import render_template
from flask import redirect
def status_401(error):
    return redirect("/login")
    
def status_404(error):
     return render_template("404error.html")

app = create_app()
    
if __name__ == "__main__":
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port = 3000, debug=True)