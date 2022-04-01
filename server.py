'''
Servicio Web que escucha en el puerto 12345
y tiene dos endpoints
una que guarda la cadena que se le envia como parámetro en un fichero
y otro que devuelve el número de veces de una cadena aparece al menos una vez
en cada una de las lineas del fichero, ignorando mayúsculas y tildes

@autor: Jorge Sánchez-Alor, Antonio De Gea Velasco, Adrian Rodriguez Montesinos

'''

# ***IMPORTS*** #
# Empleamos la biblioteca FLASK para implementar el servicio web
from flask import Flask
# Para la base de datos y la encriptacion
from flask_sqlalchemy import SQLAlchemy

# Para hacer uso de argumentos
import argparse

# Parámetros por defecto y configuración
import config.default

db = SQLAlchemy()


def create_app():
    # La aplicación a partir de la clase Flask
    app = Flask(__name__)
    #SECRET_KEY generada mediante secrets.token_hex()
    app.config['SECRET_KEY'] = config.default.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.default.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.default.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    # Registro de los Blueprints
    from endpoints.public import public_bp
    app.register_blueprint(public_bp)

    from endpoints.private import private_bp
    app.register_blueprint(private_bp)

    return app

# *** METODOS *** #
# Comprobación de argumentos
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", '--file', type=str, help="nombre del fichero de persistencia", required=False, default=config.default.FILENAME)
    parser.add_argument("-p", '--port', type=int, help="numero de puerto de escucha", required=False, default=config.default.PORT)
    args = parser.parse_args()

    print("Escuchando en puerto: ", args.port)
    return args.file, args.port

# DEPRECATED
# Comprobación existencia del fichero de persistencia
def check_file(fichero):
    try:
        with open(fichero, "x") as f: #Si el fichero existe lanza una excepcion
            print("Creando fichero de persistencia: " + fichero)
            return 0

    except FileExistsError:
        print("Encontrado fichero de persistencia...")
        print("Cargando datos de " + fichero)
        return 1


# Para que se inicie la aplicación al ejecutar el script
# (Esto se excluye del test porque
# check_file() tiene su propio test
# main() tiene también su propio test
# y app.run() depende de Flask)
if __name__ == "__main__": #pragma: no cover
    file, port = main()
    check_file(file)
    app = create_app()
    app.run(host=config.default.HOST, port=port, ssl_context='adhoc')
