from flask import render_template, abort
from app.models import User, Permission, Role
from flask_admin.contrib.sqla import ModelView
from . import main
from .. import db, admin
from ..decorator import permission_required
from flask_login import login_required, current_user

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))


@main.route('/')
@main.route("/index")
def index():
    """
    View function for the home page. It displays a list of news articles.
    """
    news_list = [
        {'title': 'Healthy food ',
         'url': 'https://russian.rt.com/russia/news/1321691-rebenok-zdorovaya-pischa',
         'description': 'Russians were told how to instill in their children a love of healthy food'},
        {'title': 'Russian SWIFT',
         'url': 'https://swentr.site/business/598624-g7-eu-sanctions-russian-swift/',
         'description': 'West eyeing ‘Russian SWIFT’ as sanctions target – Bloomberg'},
        {'title': 'The Sun',
         'url': 'https://ria.ru/20240601/vspyshki-1949909017.html',
         'description': 'Two powerful flares occurred on the Sun'},
        {'title': 'Food',
         'url': 'https://ria.ru/20240508/pischa-1944558593.html?in=t',
         'description': " what foods shouldn't eat on days of magnetic storms"},
        {'title': 'Arsenal',
         'url': 'https://rsport.ria.ru/20240601/rpl-1949921341.html',
         'description': 'Nizhny Novgorod beat Arsenal Tula and remained in the RPL'},
        {'title': '“The Boy’s Word ”',
         'url': 'https://ria.ru/20240530/serial-1949529727.html',
         'description': 'the best in the “Strength in Truth” category at the IRI Awards'},
        {'title': 'A plant',
         'url': 'https://nauka.tass.ru/nauka/20966151?utm_source=tass.ru&utm_medium=referral&utm_campaign=tass.ru&utm_referrer=tass.ru',
         'description': 'A plant has been created that reduces water hardness by six times'},
        {'title': 'In China...',
         'url': 'https://nauka.tass.ru/nauka/20963967',
         'description': "They created a membrane made of nanotubes that ..."},
        {'title': 'The Hermitage ',
         'url': 'https://tass.ru/kultura/20969753',
         'description': 'Organized concerts of Baroque music for the exhibition '},
        {'title': 'The Starliner ',
         'url': 'https://tass.ru/kosmos/20969275',
         'description': "The first manned launch of the Starliner spacecraft to the ISS "}
    ]
    return render_template('index.html', news_list=news_list)


@main.route("/error")
def test_error():
    """
    View function to test error handling by aborting with a 404 status code.
    """
    abort(404)


@main.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderator():
    """
    View function for moderators. Requires the user to be logged in and have moderate permissions.
    """
    return "For moderator"


@main.route("/secret")
@login_required
def secret():
    """
    View function that is accessible only to authenticated users.
    """
    return "Only for auth"


@main.route("/testConfirm")
def testConfirm():
    """
    View function to test user email confirmation. Generates a confirmation token for the first user.
    """
    user = User.query.filter_by().first()
    tmp = user.generate_confirmation_token()
    user.confirm(tmp)


@main.route('/user/<username>')
def user(username):
    """
    View function to display a user's profile page based on their username.
    """
    user = User.query.filter_by(username=username).first_or_404()
    role = Role.query.get(user.role_id)
    return render_template('profile.html', user=user, role=role)


@main.route('/profile')
@login_required
def profile():
    """
    View function to display the profile page of the currently logged-in user.
    """
    profile_data = current_user
    role = Role.query.get(profile_data.role_id)
    return render_template('profile.html', user=profile_data, role=role)
