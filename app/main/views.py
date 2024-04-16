import random

import flask

from flask import request, make_response, render_template, redirect, url_for, session
from app.main.forms import SimpleForm

from app.models import User
from flask_mail import Message

from . import main
from .. import mail
from flask_login import login_required

'''from app.models import db'''


@main.route('/')
@main.route("/index")
def index():
    default_user = {"username": "Kseniya"}
    session_text = session.get('text')
    if session_text is not None or session_text != "":
        return render_template("index.html", text=session_text, auth=session.get('auth'))
    else:
        return render_template('index.html', user=default_user, auth=session.get('auth'))


@main.route("/cookie")
def cookie():
    user_agent = request.headers.get('User-Agent')
    if 'Mozilla' in user_agent:
        flag = random.randint(1, 100)
        res = make_response('<h1>Browser correct. Cookie is set</h1>')
        res.set_cookie('flag', str(flag))
        return res
    else:
        return '<h1>Incorrect browser! Your browser is {}!</h1>'.format(user_agent)


@main.route('/index/testForm', methods=['GET', 'POST'])
def testForm():
    text = None
    form = SimpleForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.password == form.password.data:
                session['auth'] = True
                confirm(user)
                return redirect(url_for('index'))
            else:
                session['auth'] = False
                session['text'] = 'Incorrect password or login, please try again'
        else:
            session['auth'] = False
        return redirect(url_for('index'))
    return render_template('formTemplate.html', form=form, text=text, auth=session.get('auth'))


'''
@main.route('/logout')
def logout():
    if session.get('auth'):
        session['auth'] = False
        session['text'] = None
    return redirect(url_for('index'))
'''


def confirm(user):
    send_mail("xenya.dmitrievna@gmail.com", 'HomeBank Community Team', 'send_mail', user=user)
    redirect(url_for('index'))


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject,
                  sender=main.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    mail.send(msg)


@main.route("/secret")
@login_required
def secret():
    return "Only for auth"
