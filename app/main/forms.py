from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo


class SimpleForm(FlaskForm):
    username = StringField(" Username: ")
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Log in")
