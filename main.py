from flask import Flask
from flask_bootstrap import Bootstrap5


flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = "hard to unlock"

from app import routes

if __name__ == "__main__":
    flask_app.run(debug=True)

bootstrap = Bootstrap5(flask_app)
