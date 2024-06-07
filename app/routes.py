from app import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,"night.db")
db = SQLAlchemy()
db.init_app(app)

import app.models as models

@app.route('/')
def home():
    return render_template('home.html')
