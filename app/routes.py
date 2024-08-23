from app import app
from flask import render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, IMAGES, UploadSet
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "night.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_IMAGES_DEST'] = '/static/images'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
app.secret_key = 'Very$ecret'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'pa$$w0rd'
db = SQLAlchemy(app)

import app.models as models
from app.forms import RegistrationForm, LoginForm, Add_Star, Add_Constellation
from app.models import db, User


def signed_in():
    # checks if user is signed in, returns username or none
    if 'user' in session.keys():
        return session['user']
    else:
        return 'none'


def is_admin():
    # checks if user is admin, returns 1 or 0 to represent admin vs not.
    if 'admin' in session.keys():
        return session['admin']
    else:
        return 0


@app.route('/')
def home():
    person = signed_in()
    admin = is_admin()
    return render_template('home.html', message='home', person=person, admin=admin)


@app.route('/all_months')
def all_months():
    person = signed_in()
    admin = is_admin()
    months = models.Month.query.all()
    return render_template('all_months.html', months=months, person=person, admin=admin)


@app.route('/month/<int:id>')
def month(id):
    person = signed_in()
    admin = is_admin()
    month = models.Month.query.filter_by(id=id).first()
    return render_template('month.html', month=month, person=person, admin=admin)


@app.route('/all_planets')
def all_planets():
    person = signed_in()
    admin = is_admin()
    planets = models.Planet.query.all()
    return render_template('all_planets.html', planets=planets, person=person, admin=admin)


@app.route('/planet/<int:id>')
def planet(id):
    person = signed_in()
    admin = is_admin()
    planet = models.Planet.query.filter_by(id=id).first()
    return render_template('planet.html', planet=planet, person=person, admin=admin)


@app.route('/all_stars')
def all_stars():
    person = signed_in()
    admin = is_admin()
    stars = models.Star.query.all()
    return render_template('all_stars.html', stars=stars, person=person, admin=admin)


@app.route('/star/<int:id>')
def star(id):
    person = signed_in()
    admin = is_admin()
    star = models.Star.query.filter_by(id=id).first()
    return render_template('star.html', star=star, person=person, admin=admin)


@app.route('/all_constellations')
def all_constellations():
    person = signed_in()
    admin = is_admin()
    constellations = models.Constellation.query.all()
    return render_template('all_constellations.html', constellations=constellations, 
                           person=person, admin=admin)


@app.route('/constellation/<int:id>')
def constellation(id):
    person = signed_in()
    admin = is_admin()
    constellation = models.Constellation.query.filter_by(id=id).first()
    star = models.Star.query.filter_by(constellation=id).first()
    return render_template('constellation.html', constellation=constellation, 
                           person=person, star=star, admin=admin)


@app.route('/add_data')
def add_data():
    person = signed_in()
    admin = is_admin()
    if person == 'none':
        return render_template("404.html", person=person, admin=admin), 404
    return render_template('add_data.html', person=person, admin=admin)


@app.route('/add_star', methods=['GET', 'POST'])
def add_star():
    person = signed_in()
    admin = is_admin()
    if person == 'none':
        return render_template("404.html", person=person, admin=admin), 404
    form = Add_Star()
    form.constellation.query = models.Constellation.query.all()
    form.stage.query = models.Lifecycle.query.all()
    if request.method == 'GET':
        return render_template('add_star.html', form=form, person=person, admin=admin)
    else:
        if form.validate_on_submit():
            new_star = models.Star()
            new_star.name = form.name.data
            new_star.description = form.description.data
            new_star.constellation = form.constellation.data
            new_star.image = form.image.data
            new_star.stage = form.stage.data
            db.session.add(new_star)
            db.session.commit()
            return redirect(url_for('add_star'))
        else:
            return render_template('add_star.html', person=person, admin=admin)


@app.route('/add_constellation', methods=['GET', 'POST'])
def add_constellation():
    person = signed_in()
    admin = is_admin()
    if person == 'none':
        return render_template("404.html", person=person, admin=admin), 404
    form = Add_Constellation()
    if request.method == 'GET':
        return render_template('add_constellation.html', form=form, person=person, admin=admin)
    else:
        if form.validate_on_submit():
            new_constellation = models.Constellation()
            new_constellation.name = form.name.data
            new_constellation.description = form.description.data
            new_constellation.story = form.story.data
            new_constellation.image = form.image.data
            db.session.add(new_constellation)
            db.session.commit()
            return redirect(url_for('add_constellation'))
        else:
            return render_template('add_constellation.html', person=person, admin=admin)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    admin = is_admin()
    person = signed_in()
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('create_user.html', form=form, person=person, admin=admin)
    else:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            session['user'] = username
            info = models.User.query.filter_by(username=username).first()
            session['admin'] = info.admin
            user = User.query.filter_by(username=username).first()
            person = session['user']
            if 'admin ' in session.keys():
                admin = session['admin']
            return redirect(url_for('home'), person=person, admin=admin)
        return render_template('create_user.html', form=form, person=person, admin=admin)


@app.route('/login', methods=['GET', 'POST'])
def login():
    person = signed_in()
    admin = is_admin()
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Logged in successfully!')
            session['user'] = username
            person = session['user']
            # Retreive account info from database
            info = models.User.query.filter_by(username=person).first()
            session['admin'] = info.admin
            admin = session['admin']
            return render_template('home.html', person=person, admin=admin)
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form, person=person, admin=admin)


@app.route('/clear_user')
def clear_user():
    session.clear()
    session.pop('user', None)
    session.pop('admin', None)
    person = signed_in()
    admin = is_admin()
    return render_template('home.html', message='Logged out', person=person, admin=admin)


@app.route('/delete_constellation/<int:id>', methods=['GET', 'POST'])
def delete_constellation(id):
    person = signed_in()
    admin = is_admin()
    if admin == 0:
        return render_template("404.html", person=person, admin=admin), 404
    constellation = models.Constellation.query.get_or_404(id)
    db.session.delete(constellation)
    db.session.commit()
    return redirect(url_for('all_constellations', person=person, admin=admin))


@app.route('/delete_star/<int:id>', methods=['GET', 'POST'])
def delete_star(id):
    person = signed_in()
    admin = is_admin()
    if admin == 0:
        return render_template("404.html", person=person, admin=admin), 404
    star = models.Star.query.get_or_404(id)
    db.session.delete(star)
    db.session.commit()
    return redirect(url_for('all_stars', person=person, admin=admin))


@app.errorhandler(404)
def not_found(e):
    person = signed_in()
    admin = is_admin()
    return render_template("404.html", person=person, admin=admin), 404
