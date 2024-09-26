from app.routes import db
from werkzeug.security import generate_password_hash, check_password_hash


ConstellationMonth = db.Table('ConstellationMonth',
                              db.Column('cid', db.Integer, db.ForeignKey('Constellation.id')),
                              db.Column('mid', db.Integer, db.ForeignKey('Month.id')),
                              )


PlanetMonth = db.Table('PlanetMonth',
                       db.Column('pid', db.Integer, db.ForeignKey('Planet.id')),
                       db.Column('mid', db.Integer, db.ForeignKey('Month.id')),
                       )


class Month(db.Model):
    __tablename__ = "Month"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    constellations = db.relationship('Constellation',
                                     secondary='ConstellationMonth',
                                     back_populates='months')
    planets = db.relationship('Planet',
                              secondary='PlanetMonth',
                              back_populates='months')

    def __repr__(self):
        return self.name


class Constellation(db.Model):
    __tablename__ = "Constellation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    story = db.Column(db.Text())
    image = db.Column(db.Text())
    months = db.relationship('Month',
                             secondary='ConstellationMonth',
                             back_populates='constellations')

    def __repr__(self):
        return self.name


class Planet(db.Model):
    __tablename__ = "Planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    image = db.Column(db.Text())
    order = db.Column(db.Integer)
    distance = db.Column(db.Text())
    months = db.relationship('Month',
                             secondary='PlanetMonth',
                             back_populates='planets')

    def __repr__(self):
        return self.name


class Star(db.Model):
    __tablename__ = "Star"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    constellation = db.Column(db.Integer, db.ForeignKey("Constellation.id"))
    constellation_desc = db.relationship("Constellation", backref="Star")
    image = db.Column(db.Text())
    stage = db.Column(db.Integer, db.ForeignKey("Lifecycle.id"))
    stage_desc = db.relationship("Lifecycle", backref="Star")

    def __repr__(self):
        return self.name


class Lifecycle(db.Model):
    __tablename__ = "Lifecycle"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())

    def __repr__(self):
        return self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return self.username
