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


@app.route('/all_planets')
def all_planets():
    planets = models.Planet.query.all()
    return render_template('all_planets.html', planets=planets)


@app.route('/all_stars')
def all_stars():
    stars = models.Star.query.all()
    return render_template('all_stars.html', stars=stars)


@app.route('/all_constellations')
def all_constellations():
    constellations = models.Constellation.query.all()
    return render_template('all_constellations.html', constellations=constellations)
