import random

import flask

from flask import request, make_response, render_template, redirect, url_for, session, flash
from app.main.forms import SimpleForm

from app.models import User
from flask_mail import Message
from . import main
from .. import mail
from app import db
from flask_login import login_required


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
        user = db.session.query(User).filter(User.username == form.text.data).first()
        if user is not None:
            if user.password == form.password.data and user.email == form.email.data:
                flash("Thanks for log in!", "success")
                session[
                    'text'] = "Thanks for log in! Your login: " + user.email + " and your password: " + user.password
                form.text.data = ''
                session['auth'] = True
                confirm(user)
                return redirect(url_for('index'))
            else:
                flash("Not correct password or email", "error")
                session['auth'] = False
        else:
            flash("No such user", "warning")
            session['auth'] = False
    return render_template('formTemplate.html', form=form, text=text)


@main.route('/logout')
def logout():
    if session.get('auth'):
        session['auth'] = False
        session['text'] = None
    return redirect(url_for('main.index'))


def confirm(user):
    send_mail(user.email, 'Create new user', 'send_mail', user=user)


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


@main.route("/testConfirm")
def testConfirm():
    user = User.query.filter_by().first()
    tmp = user.generate_confirmation_token()
    user.confirm(tmp)
