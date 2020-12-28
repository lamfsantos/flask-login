from flask import Blueprint, render_template, request, make_response, wrappers
from services import user as service
from datetime import timedelta
from configs import general as configs
# import service.tarifas as tarifas
# import service.planos as planos

user_blueprint = Blueprint("index", __name__, static_folder="static", template_folder="templates")

@user_blueprint.route('/')
def index():
    return render_template("index.html")

@user_blueprint.route('/token', methods= ['POST'])
def login_for_access_token():
    #print(request.form.keys()[0])
    auth = dict(request.form)
    # print(f['username'])
    # print('aaaaaaaaa')
    # return 'aaa'
    user = service.authenticate_user(auth['username'], auth['password'])
    if not user:
        return make_response(
            'Incorrect username or password',
            401,
            {"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_blueprint.route("/logged")
def logged():
    token = request.headers.get('Authorization')
    resp = service.get_current_user(token)
    print(resp)
    print(type(resp))
    if type(resp) == wrappers.Response:
        return {"detail":"Not authenticated"}

    #pegar o header do request e fazer a validação
    return render_template(
        'logged.html'
    )
