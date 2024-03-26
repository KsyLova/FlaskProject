import random

import flask
from flask import request, make_response, render_template, redirect, url_for, session
from app.forms import SimpleForm
from main import flask_app
from models import User


@flask_app.route('/')
@flask_app.route("/index")
def index():
    default_user = {"username": "Kseniya"}
    session_text = session.get('text')
    if session_text is not None or session_text != "":
        return render_template("index.html", text=session_text, auth=session.get('auth'))
    else:
        return render_template('index.html', user=default_user, auth=session.get('auth'))


@flask_app.route("/cookie")
def cookie():
    user_agent = request.headers.get('User-Agent')
    if 'Mozilla' in user_agent:
        flag = random.randint(1, 100)
        res = make_response('<h1>Browser correct. Cookie is set</h1>')
        res.set_cookie('flag', str(flag))
        return res
    else:
        return '<h1>Incorrect browser! Your browser is {}!</h1>'.format(user_agent)


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@flask_app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@flask_app.route("/1")
def error500():
    flask.abort(500)


@flask_app.route('/index/testForm', methods=['GET', 'POST'])
def testForm():
    text = None
    form = SimpleForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.password == form.password.data:
                session['auth'] = True
                session['text'] ="Hello,"+ user.username
            else:
                session['auth'] = False
                session['text'] = 'Incorrect password or login, please try again'
        else:
            session['auth'] = False
        return redirect(url_for('index'))
    return render_template('formTemplate.html', form=form, text=text, auth=session.get('auth'))


@flask_app.route('/logout')
def logout():
    if session.get('auth'):
        session['auth'] = False
        session['text'] = None
    return redirect(url_for('index'))
