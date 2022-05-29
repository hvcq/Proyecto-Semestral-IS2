"""Archivo ejecutable"""
from application import create_app
from flask import redirect
def status_401(error):
    return redirect("/login")
    
def status_404(error):
    return "<h1>Página no encontrada</h1>"

app = create_app()
    
if __name__ == "__main__":
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port = 3000, debug=True)