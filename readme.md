# Para operar la base de datos de forma manual

*Añadir dependencias descargadas aca pls. 

* Borrar base de datos manualmente
$python
>>> from wsgi import create_app
>>> from application.__init__ import db
>>> db.drop_all(app=create_app())

* Crear base de datos manualmente
$python
>>> from wsgi import create_app
>>> from application.__init__ import db
>>> db.create_all(app=create_app())

_ Solo borrara y creara lo que se añadio en routes.py _