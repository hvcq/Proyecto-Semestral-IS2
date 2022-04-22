# Flask Website

Sistema de encuestas desarrollado en Flask.

## Instalación

Usa el administrador de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar virtualenv usando privilegios de administrador (Suponiendo que ya tienes instalado python)
>>> db.create_all(app=create_app())

```bash
pip install virtualenv
```
Crearemos el entorno virtual con el siguiente comando (**Ojo**: Instalarlo la carpeta del proyecto)

```bash
virtualenv venv
```

Para iniciar el entorno virtual bastará dirigirse a la carpeta creada anteriormente, luego **Scripts** y ejecutar el siguiente comando.

```bash
activate
```

Para desactivar el entorno solo se necesita el comando.

```bash
deactivate
```

Por ultimo es necesario installar flask utilizando:

```bash
pip install Flask
```

Agregaremos una libreria interezante para la validacion de formularios.

```bash
pip install Flask-WTF
pip install email-validator
```

## Uso

Luego seteamos la variable de entorno de la siguiente manera:

*En Windows*

```bash
set FLASK_APP=nombre_archivo.py
flask run
```

*En Linux*

```bash
export FLASK_APP=nameFile
flask run
```

Otro aspecto relevante es usar el modo debug para actualizar 
automaticamente la web.

*En Windows*

```bash
set FLASK_ENV=development
flask run
```

*En Linux*
```bash
export FLASK_ENV=development
```