from app import app
from flask import render_template, redirect, url_for, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, IMAGES, UploadSet
import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "night.db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_IMAGES_DEST'] = os.path.join(basedir, 'static/images')
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
app.secret_key = 'Very$ecret'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'pa$$w0rd'
db = SQLAlchemy(app)

import app.models as models
from app.forms import RegistrationForm, LoginForm, Add_Star, Add_Constellation
from app.models import db, User, Constellation, Star


def signed_in():
    # needed in every route that renders navbar to check if
    # it should say login or log out
    if 'user' in session.keys():
        return session['user']
    else:
        return None


def is_admin():
    # checks if user is admin, returns 1 or None admin vs not.
    if 'admin' in session.keys():
        return session['admin']
    else:
        return None


def present_month():
    # returns month data for current month
    id = datetime.datetime.now().strftime("%m")
    month = models.Month.query.filter_by(id=id).first_or_404()
    return month


@app.route('/')
def home():
    person = signed_in()
    month = present_month()  # used to display information on current month
    return render_template('home.html', person=person, month=month)


@app.route('/month/<int:id>')
def month(id):
    person = signed_in()
    # first_or_404() so if data can not be grabbed 404s such as if id=0
    month = models.Month.query.filter_by(id=id).first_or_404()
    return render_template('month.html', month=month, person=person)


@app.route('/all_planets')
def all_planets():
    person = signed_in()
    planets = models.Planet.query.all()
    return render_template('all_planets.html', planets=planets, person=person)


@app.route('/planet/<int:id>')
def planet(id):
    person = signed_in()
    planet = models.Planet.query.filter_by(id=id).first_or_404()
    return render_template('planet.html', planet=planet, person=person)


@app.route('/all_stars')
def all_stars():
    person = signed_in()
    stars = models.Star.query.all()
    return render_template('all_stars.html', stars=stars, person=person)


@app.route('/star/<int:id>')
def star(id):
    person = signed_in()
    admin = is_admin()  # needs admin so that delete button can appear
    star = models.Star.query.filter_by(id=id).first_or_404()
    return render_template('star.html', star=star, person=person, admin=admin)


@app.route('/all_constellations')
def all_constellations():
    person = signed_in()
    constellations = models.Constellation.query.all()
    return render_template('all_constellations.html',
                           constellations=constellations, person=person)


@app.route('/constellation/<int:id>')
def constellation(id):
    person = signed_in()
    admin = is_admin()  # need admin so that delete button can appear
    constellation = models.Constellation.query.filter_by(id=id).first_or_404()
    stars = models.Star.query.filter_by(constellation=id).all()
    return render_template('constellation.html', constellation=constellation,
                           person=person, stars=stars, admin=admin)


@app.route('/add_data')
def add_data():
    person = signed_in()
    # only lets signed in users add_data
    if person is None:
        return render_template('sign_in.html')
    return render_template('add_data.html', person=person)


@app.route('/add_star', methods=['GET', 'POST'])
def add_star():
    person = signed_in()
    if person is None:
        return render_template('sign_in.html')
    form = Add_Star()
    form.constellation.query = models.Constellation.query.all()
    form.stage.query = models.Lifecycle.query.all()
    if form.validate_on_submit():
        # makes sure star doesn't already exists
        existing_star = Star.query.filter_by(name=form.name.data).first()
        # not first_or_404() because need to know when is None
        if existing_star:
            flash('Star already exists.')
            return render_template('add_star.html', form=form, person=person)
        new_star = models.Star()
        new_star.name = form.name.data
        new_star.description = form.description.data
        if form.constellation.data:
            new_star.constellation = form.constellation.data.id
        else:
            new_star.constellation = None
        if form.image.data:
            new_star.image = images.save(form.image.data)
        else:
            # if no image is uploaded it uploads a basic image to match styling
            new_star.image = "basic.jpg"
        new_star.stage = form.stage.data.id
        db.session.add(new_star)
        db.session.commit()
        return redirect(url_for('all_stars'))
    else:
        # displays errors to user
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{error}")
        return render_template('add_star.html', form=form, person=person)


@app.route('/add_constellation', methods=['GET', 'POST'])
def add_constellation():
    person = signed_in()
    if person is None:
        return render_template('sign_in.html')
    form = Add_Constellation()
    form.months.query = models.Month.query.all()
    if form.validate_on_submit():
        # makes sure constellation doesn't already exists
        file = form.name.data
        query = Constellation.query.filter_by(name=file)
        existing_constellation = query.first()
        # not first_or_404() because most times result will be None
        if existing_constellation:
            flash('Constellation already exists.')
            return render_template('add_constellation.html',
                                   form=form, person=person)
        new_constellation = models.Constellation()
        new_constellation.name = form.name.data
        new_constellation.description = form.description.data
        new_constellation.story = form.story.data
        if form.image.data:
            new_constellation.image = images.save(form.image.data)
        else:
            # if no image is uploaded it uploads a basic image to match styling
            new_constellation.image = "basic.jpg"
        new_constellation.months.extend(form.months.data)
        db.session.add(new_constellation)
        db.session.commit()
        return redirect(url_for('all_constellations'))
    else:
        # displays errors to user
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{error}")
        return render_template('add_constellation.html',
                               form=form, person=person)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    person = signed_in()
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # makes sure username doesn't already exists
        existing_user = User.query.filter_by(username=username).first()
        # not first_or_404() because most times result will be None
        if existing_user:
            flash('Username already exists.'
                  'Please choose a different username.')
            return render_template('create_user.html', form=form,
                                   person=person)
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session['user'] = username
        info = models.User.query.filter_by(username=username).first_or_404()
        session['admin'] = info.admin
        user = User.query.filter_by(username=username).first_or_404()
        # create session so other routes can check if logged in
        person = session['user']
        flash(f'Welcome {username}!')
        month = present_month()  # need month because rendering the home page
        return render_template('home.html', person=person, month=month)
    # displays errors to user
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{error}")
    return render_template('create_user.html', form=form, person=person)


@app.route('/login', methods=['GET', 'POST'])
def login():
    person = signed_in()
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Logged in successfully!')
            # create session so other routes can check if logged in
            session['user'] = username
            # updates person variable as the session has been changed
            person = session['user']
            info = models.User.query.filter_by(username=person).first()
            # creates session so admin can be accessed on other routes
            session['admin'] = info.admin
            # need month because rendering the home page
            month = present_month()
            return render_template('home.html', person=person, month=month)
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form, person=person)


@app.route('/clear_user')
def clear_user():
    session.clear()
    session.pop('user', None)
    session.pop('admin', None)
    flash('Logged out Succesfully!')
    return redirect(url_for('home'))


@app.route('/delete_constellation/<int:id>', methods=['GET', 'POST'])
def delete_constellation(id):
    admin = is_admin()  # need admin because only admins can delete
    if admin != 1:
        abort(401)
    constellation = models.Constellation.query.get_or_404(id)
    db.session.delete(constellation)
    db.session.commit()
    return redirect(url_for('all_constellations'))


@app.route('/delete_star/<int:id>', methods=['GET', 'POST'])
def delete_star(id):
    admin = is_admin()  # need admin because only admins can delete
    if admin != 1:
        abort(401)
    star = models.Star.query.get_or_404(id)
    db.session.delete(star)
    db.session.commit()
    return redirect(url_for('all_stars'))


@app.errorhandler(404)
def error404(error):
    person = signed_in()
    return render_template("404.html", person=person, error=error)


@app.errorhandler(401)
def error4014(error):
    person = signed_in()
    return render_template("401.html", person=person, error=error)
