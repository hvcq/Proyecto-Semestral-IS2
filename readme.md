# Uso de la aplicacion de encuestas

Antes de correr la aplicacion es necesario instalar algunas dependecias, estas dependencias se instalan a traves del comando ***pip install nombre_dependencia***
## Nombre de dependencias necesarias para su funcionamiento

* Flask
* Flask-SQLAlchemy
* Flask-Flash
* SQLAlchemy
* numpy (para hacer matrices n-dimensionales)
* psycopg2 (permite el uso de Postresql con SQLAlchemy)
* ddtrace (Permite rastrear solicitudes al servidor)
* python-dotenv (Permite entregar la configuración del servidor a traves de un archivo)
* flask-mail (Para enviar emails usando flask)

Luego para ejecutar la aplicacion se debe ir al directorio donde esta el archivo ***wsgi.py*** y a continuacion abrir la terminar e ingresar:

### Para Windows:
```bash
python wsgi.py
```
### Para Linux:
```bash
python3 wsgi.py
```

Por defecto al ejecutar la aplicacion se borraran los datos de la base de datos en el schema public de la misma. Para que esto no ocurra se deben comentar las instrucciones db.drop_all() y db.create_all() en ***application/__init__.py***

Para hacer la eliminacion y creacion de la base de datos de forma manual se deben seguir los respectivos procedimientos señalados a continuacion:
## Eliminar datos de la base de datos de forma manual

Primero ingresar a la terminal de **python**, luego ingresar:
```bash
from wsgi import create_app
```
```bash
from application.__init__ import db
```
```bash
db.drop_all(app=create_app())
```
## Crear base de datos manualmente

Primero ingresar a la terminal de **python**, luego ingresar:
```bash
from wsgi import create_app
```
```bash
from application.__init__ import db
```
```bash
db.create_all(app=create_app())
```
