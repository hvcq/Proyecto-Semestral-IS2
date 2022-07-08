# Uso de la aplicacion de encuestas

Antes de correr la aplicacion es necesario instalar algunas dependecias, estas dependencias se instalan a traves del comando ***pip install nombre_dependencia***
## Nombre de dependencias necesarias para su funcionamiento
* virtualenv (para entornos virtuales, necesario para varias librerias)
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* psycopg2 (permite el uso de Postresql con SQLAlchemy)
* ddtrace (Permite rastrear solicitudes al servidor)
* python-dotenv (Permite entregar la configuración del servidor a traves de un archivo)
* flask-mail (Para enviar emails usando flask)
* flask-login (Para control de login y vistas)
* flask-WTF (Para creacion de token de password)

Luego para ejecutar la aplicacion se debe ir al directorio donde esta el archivo ***wsgi.py*** y a continuacion abrir la terminar e ingresar:

### Para Windows:
```bash
python wsgi.py
```
### Para Linux:
```bash
python3 wsgi.py
```

Para que el programa funcione debe estar conectado a una base de datos, esta se
proporciona en el archivo ***.env*** ubicado en el directorio raiz.
Al abrirlo se debe modificar el apartado "SQLALCHEMY_DATABASE_URI", donde despues
del signo de igual (=) se debe escribir la ruta de la base de datos.
(Para un correcto funcionamiento se recomienda utilizar una base de datos PostgreSQL)

### Ejemplo de una ruta valida:
```bash
SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@localhost:5432/encuestas
```

Por ultimo para que se creen las tablas en el nuevo esquema de la base de datos
asignado se debe ir al archivo ***application/__init__.py*** y descomentar la
instruccion db.create_all(), de esta manera al ejecutar el programa se llamara
a este metodo y se crearan las tablas en el esquema. Luego se puede volver a
comentar la instruccion pues es necesario hacer esto solo una vez.