from app import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "night.db")
db = SQLAlchemy()
db.init_app(app)

import app.models as models


@app.route('/')
def home():
    return render_template('home.html')


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


@app.errorhandler(404) 
def not_found(e):
    return render_template("404.html"), 404
