import os
from flask import Flask
from flask_bootstrap import Bootstrap5

basedir = os.path.abspath(os.path.dirname(__file__))

flask_app = Flask(__name__)


from app import routes

if __name__ == "__main__":
    flask_app.run(debug=True)

bootstrap = Bootstrap5(flask_app)



