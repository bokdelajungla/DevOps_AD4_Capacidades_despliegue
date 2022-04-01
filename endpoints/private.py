from flask import request, jsonify, make_response
from flask import Blueprint
from functools import wraps
import jwt

import config.default
from models.entitys import Users, Cadenas

# Hacemos uso de la biblioteca unicodedata para tratar las tildes y caracteres epeciales
import unicodedata



private_bp = Blueprint('private', __name__, template_folder='templates')


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, config.default.SECRET_KEY, algorithms="HS256")
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator

# El endpoint "almacena"
'''
El endpoint recibe la cadena como parámetro y la guarda en una nueva línea del fichero FILENAME
El nombre del parámetro es 'string'
la petición tiene el formato /almacena?string
Devuelve:
    * una respuesta HTML 200 OK con un json en el cuerpo indicando que el mensaje se ha creado correctamente
    * una respuesta HTML 400 BAD REQUEST con un json en el cuerpo si la petición no es correcta
'''


@private_bp.route("/almacena", methods=['POST'])
@token_required
def almacenar(current_user):
    if request.method == 'POST':
        if 'string' in request.args:
            cadena = request.args.get('string')
            with open(config.default.FILENAME, "a+") as f:
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


@private_bp.route("/consulta", methods=['GET'])
@token_required
def consultar(current_user):
    if request.method == 'GET':
        if 'string' in request.args:
            cadena = request.args.get('string')
            if " " not in cadena:
                with open(config.default.FILENAME, "r") as f:
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


@private_bp.route("/logout", methods=['GET', 'POST'])
@token_required
def logout():
    return "Logout"