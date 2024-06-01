from flask import render_template, redirect, request, flash, url_for
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from threading import Thread
from app import mail


@auth.before_app_request
def before_request():
    """
    Function that runs before each request. It pings the current user to update their last seen timestamp.
    If the user is authenticated but not confirmed, they are redirected to the unconfirmed page.
    """
    if current_user.is_authenticated:
        current_user.ping()
        if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    View function for the login page. If the user is already authenticated, they are redirected to the index page.
    If the form is submitted and validated, the user is logged in.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_verify(form.password.data):
            login_user(user, form.remember_me.data)
            if not user.confirmed:
                return redirect(url_for("auth.unconfirmed"))
            return redirect(url_for("main.index"))
        flash('Invalid username or password')
    return render_template("auth/login.html", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    View function for the registration page. If the user is already authenticated, they are redirected to the index page.
    If the form is submitted and validated, a new user is created and a confirmation email is sent.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password = form.password.data
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_confirm(user, token)
        flash("Registration complete! Please check your email to confirm your account.")
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html", form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    View function for confirming a user's email address. If the token is valid, the user's account is confirmed.
    """
    print(token)
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash("Подтверждение успешно!")
    else:
        flash("Ссылка не валидна или ее срок действия истек")
    return redirect(url_for('main.index'))


def send_confirm(user, token):
    """
    Function to send a confirmation email to the user.
    """
    send_mail(user.email, 'Create your account', 'auth/confirm', user=user, token=token.decode('utf-8'))
    redirect(url_for('main.index'))


def send_mail(to, subject, template, **kwargs):
    """
    Function to send an email. Creates a new email message and starts a thread to send it asynchronously.
    """

    msg = Message(subject, sender="cenylova@gmail.com",
                  recipients=[to])
    try:

        msg.html = render_template(template + ".html", **kwargs)
    except:
        msg.body = render_template(template + ".txt", **kwargs)
    from main import flask_app
    thread = Thread(target=send_async_email, args=[flask_app, msg])
    thread.start()
    return thread


def send_async_email(app, msg):
    """
    Function to send an email asynchronously. Uses the app context to send the email.
    """
    with app.app_context():
        mail.send(msg)


@auth.route('/unconfirmed')
def unconfirmed():
    """
    View function for the unconfirmed page. If the user is anonymous or confirmed, they are redirected to the index page.
    Otherwise, the unconfirmed page is rendered.
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    else:
        return render_template('auth/unconfirmed.html')


@auth.route("/logout")
@login_required
def logout():
    """
    View function for logging out the user. The user is logged out and redirected to the index page with a flash message.
    """
    logout_user()
    flash("You are logout")
    return redirect((url_for("main.index")))
