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
from flask import Flask, request, jsonify, make_response

# Para la base de datos y la encriptacion
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
import datetime
from functools import wraps

# Hacemos uso de la biblioteca unicodedata para tratar las tildes y caracteres epeciales
import unicodedata
# Para hacer uso de argumentos
import argparse


# *** VARIABLES *** #
# Nombre del fichero de persistencia
FILENAME = "cadenas.txt" #Fichero por defecto
# Host
HOST = "127.0.0.1"
# Puerto
PORT = 12345 #Puerto por defecto

# La aplicación a partir de la clase Flask
app = Flask(__name__)
#SECRET_KEY generada mediante secrets.token_hex()
app.config['SECRET_KEY']='26e6f5689c2c07c42e85e725dcda798088cf673d3141bd17dfe3ef688457c351'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///devops_a3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


# *** METODOS *** #
# Comprobación de argumentos
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", '--file', type=str, help="nombre del fichero de persistencia", required=False, default=FILENAME)
    parser.add_argument("-p", '--port', type=int, help="numero de puerto de escucha", required=False, default=PORT)
    args = parser.parse_args()

    print("Escuchando en puerto: ", args.port)
    return args.file, args.port


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


# Con @app.route() marcamos el comportamiento que llevará a cabo nuestra aplicación
# Endpoint Home Page
@app.route("/")
def home():
    return "<h1>Servicio Web para Cadenas</h1><br>"


# El endpoint "almacena"
'''
El endpoint recibe la cadena como parámetro y la guarda en una nueva línea del fichero FILENAME
El nombre del parámetro es 'string'
la petición tiene el formato /almacena?string
Devuelve: 
    * una respuesta HTML 200 OK con un json en el cuerpo indicando que el mensaje se ha creado correctamente
    * una respuesta HTML 400 BAD REQUEST con un json en el cuerpo si la petición no es correcta
'''


@app.route("/almacena", methods=['POST'])
@token_required
def almacenar(current_user):
    if request.method == 'POST':
        if 'string' in request.args:
            cadena = request.args.get('string')
            with open(FILENAME, "a+") as f:
                f.write(cadena + '\n')
            data = {'code': 'SUCCESS', 'message': cadena + ' ADDED', 'userid': current_user.id}
            return make_response(jsonify(data), 200)
        else:
            data = {'code': 'BAD REQUEST', 'message': 'No se ha encontrado el parámetro "string"'}
            return make_response(jsonify(data), 400)


# El endpoint "consulta"
'''
El endpoint recibe la cadena como parámetro y comprueba el número de veces que aparece dentro del fichero
FILENAME
El nombre del parámetro es 'string'
Devuelve:
Devuelve: 
    * una respuesta HTML 200 OK con un json en el cuerpo indicando el número de veces que se ha encontrado la palabra
    * una respuesta HTML 400 BAD REQUEST con un json en el cuerpo si la petición no es correctauna respuesta
'''


@app.route("/consulta", methods=['GET'])
@token_required
def consultar(current_user):
    if request.method == 'GET':
        if 'string' in request.args:
            cadena = request.args.get('string')
            if " " not in cadena:
                with open(FILENAME, "r") as f:
                    contador = 0
                    for linea in f:
                        '''
                        Usamos unicodedata.normalize() para eliminar las tildes
                        con la opcion NFKD para que lo descomponga en caracteres simples + símbolos aditivos
                        lo codificamos a ASCII teniendo en cuenta sólo los caracteres simples (encode('ASCII','ignore'),
                        y lo convertimos de nuevo en cadena (decode('ASCII'))
                        Por último, usamos el método casefold() para ignorar mayúsculas
                        '''
                        cadena_aux = unicodedata.normalize('NFKD', cadena).encode('ASCII', 'ignore').decode(
                            'ASCII').casefold()
                        linea_aux = unicodedata.normalize('NFKD', linea).encode('ASCII', 'ignore').decode(
                            'ASCII').casefold()
                        if cadena_aux in linea_aux:
                            contador = contador + 1
                data = {'code': 'SUCCESS', 'Lineas en las que aparece': contador, 'userid': current_user.id}
                return make_response(jsonify(data), 200)
            else:
                data = {'code': 'BAD REQUEST', 'message': 'El parámetro debe ser una única palabra'}
                return make_response(jsonify(data), 400)
        else:
            data = {'code': 'BAD REQUEST', 'message': 'No se ha encontrado el parámetro string'}
            return make_response(jsonify(data), 400)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'], algorithm="HS256")
        #return jsonify({'token': token.decode('UTF-8')})
        return jsonify({'token': token})
    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/signup', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@app.route('/users', methods=['GET'])
def get_all_users():

    users = Users.query.all()

    result = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        result.append(user_data)

    return jsonify({'users': result})


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    return "Logout"


# Para que se inicie la aplicación al ejecutar el script
# (Esto se excluye del test porque
# check_file() tiene su propio test
# main() tiene también su propio test
# y app.run() depende de Flask)
if __name__ == "__main__": #pragma: no cover
    file, port = main()
    FILENAME = file
    PORT = port
    check_file(file)
    app.run(host=HOST, port=port, ssl_context='adhoc')
