from flask import Flask
from routes.user import user_blueprint
#from routes.resultado import resultado_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)
#pp.register_blueprint(index_blueprint)

if __name__ == "__main__":
    app.run()
