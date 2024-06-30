from app import app
from flask import render_template, redirect, request, url_for, session, make_response, request, flash
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "night.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Very$ecret'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'pa$$w0rd'
db = SQLAlchemy(app)

import app.models as models
from app.forms import RegistrationForm, LoginForm
from app.models import db, User


@app.route('/')
def home():
    if 'user' in session.keys():
        person = session['user']
    else:
        person = 'none'
    return render_template('home.html', message='home', person=person)


@app.route('/all_months')
def all_months():
    months = models.Month.query.all()
    return render_template('all_months.html', months=months)


@app.route('/month/<int:id>')
def month(id):
    month = models.Month.query.filter_by(id=id).first()
    return render_template('month.html', month=month)


@app.route('/all_planets')
def all_planets():
    planets = models.Planet.query.all()
    return render_template('all_planets.html', planets=planets)


@app.route('/planet/<int:id>')
def planet(id):
    planet = models.Planet.query.filter_by(id=id).first()
    return render_template('planet.html', planet=planet)


@app.route('/all_stars')
def all_stars():
    stars = models.Star.query.all()
    return render_template('all_stars.html', stars=stars)


@app.route('/star/<int:id>')
def star(id):
    star = models.Star.query.filter_by(id=id).first()
    return render_template('star.html', star=star)


@app.route('/all_constellations')
def all_constellations():
    constellations = models.Constellation.query.all()
    return render_template('all_constellations.html', constellations=constellations)


@app.route('/constellation/<int:id>')
def constellation(id):
    constellation = models.Constellation.query.filter_by(id=id).first()
    return render_template('constellation.html', constellation=constellation)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('create_user.html', form=form)
    else:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('create_user.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if 'user' in session.keys():
        person = session['user']
    else:
        person = 'none'
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            flash('Logged in successfully!')
            session['user'] = username
            if 'user' in session.keys():
                person = session['user']
                return render_template('home.html', person=person)
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form, person=person)


@app.route('/clear_user')
def clear_user():
    session.clear()
    session.pop('user', None)
    return render_template('home.html', message='Logged out')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
