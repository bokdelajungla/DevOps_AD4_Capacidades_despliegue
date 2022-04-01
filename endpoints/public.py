from flask import request, jsonify, make_response
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
import datetime

import config.default
from server import db
from models.entitys import Users

public_bp = Blueprint('public', __name__, template_folder='templates')

# Con @public_bp.route() marcamos el comportamiento que llevará a cabo nuestra aplicación
# Endpoint Home Page
@public_bp.route("/")
def home():
    return "<h1>Servicio Web para Cadenas</h1><br>"


@public_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=60)}, config.default.SECRET_KEY, algorithm="HS256")
        #return jsonify({'token': token.decode('UTF-8')})
        return jsonify({'token': token})
    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@public_bp.route('/signup', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})



@public_bp.route('/users', methods=['GET'])
def get_all_users():

    users = Users.query.all()

    result = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password

        result.append(user_data)

    return jsonify({'users': result})

