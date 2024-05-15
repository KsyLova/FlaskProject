import random
from flask import render_template, session, abort
from app.models import User, Permission
from . import main
from ..decorator import admin_required, permission_required
from flask_login import login_required


@main.route('/')
@main.route("/index")
def index():
    session_text = session.get('text')
    if session_text is not None or session_text != "":
        return render_template("index.html")
    else:
        return render_template('index.html')


@main.route("/error")
def test_error():
    abort(404)


@main.route("/admin")
@login_required
@admin_required
def for_admin():
    return "For admin"


@main.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderator():
    return "For moderator"


@main.route("/secret")
@login_required
def secret():
    return "Only for auth"


@main.route("/testConfirm")
def testConfirm():
    user = User.query.filter_by().first()
    tmp = user.generate_confirmation_token()
    user.confirm(tmp)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)
