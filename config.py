import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hard to unlock"
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.googlemail.com"
    MAIL_PORT = os.environ.get('MAIL_PORT') or "587"
    MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', '5870'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'cenylova@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'iypa rszq uhwv rgmg'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ADMIN = 'cenylova@gmail.com'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///flask.db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///flask.db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///flask.db'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
