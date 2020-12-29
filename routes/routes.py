from flask import request, jsonify, make_response, Blueprint, render_template
from configs import general as configs
from services.services import token_required
from services import services
from werkzeug.security import check_password_hash,generate_password_hash
import jwt
import datetime

routes_blueprint = Blueprint("index", __name__, static_folder="static", template_folder="templates")

@routes_blueprint.route('/token',  methods=['POST'])
def token():
    #auth = request.authorization
    auth = dict(request.form)

    if not auth or not auth['username'] or not auth['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = services.get_user(auth['username'])

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.hashed_password, auth['password']):
        token = jwt.encode({'username' : user.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, configs.SECRET_KEY)

        #return jsonify({'token' : token.decode('UTF-8')})
        return jsonify({'token' : token})

    return make_response('Could not verify', 401, {})

@routes_blueprint.route("/",  methods=['GET'])
def index():
    return render_template(
        'index.html'
    )

@routes_blueprint.route("/logged",  methods=['GET'])
@token_required
def logged():
    return render_template(
        'logged.html',
        test = "logged :)",
    )
