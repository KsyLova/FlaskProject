from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo


class SimpleForm(FlaskForm):
    username = StringField(" Username: ")
    # email = EmailField(" Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    # password_repeat = PasswordField("Повторите пароль: ", validators=[DataRequired(), EqualTo('password_test',
    #                                                                                       message="Пароли не совпадают")])
    # select_test = SelectField("Ваш пол:", choices=[('муж', 'мужской'), ('жен', 'женский')])
    submit = SubmitField("Log in")
