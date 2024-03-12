from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo


class SimpleForm(FlaskForm):
    text = StringField(" Введите Ваше имя: ", validators=[DataRequired()])
    email = EmailField(" Email: ", validators=[DataRequired()])
    password_test = PasswordField("Введите пароль: ", validators=[DataRequired()])
    password_repeat = PasswordField("Повторите пароль: ", validators=[DataRequired(), EqualTo('password_test',
                                                                                          message="Пароли не совпадают")])
    select_test = SelectField("Ваш пол:", choices=[('муж', 'мужской'), ('жен', 'женский')])
    submit = SubmitField("Зарегистрироваться")
