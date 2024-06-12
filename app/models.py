from app.routes import db


class Month(db.Model):
    __tablename__ = "Month"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())

    def __repr__(self):
        return self.name


class Constellation(db.Model):
    __tablename__ = "Constellation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    story = db.Column(db.Text())
    image = db.Column(db.Text())

    def __repr__(self):
        return self.name


class Planet(db.Model):
    __tablename__ = "Planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    constellation = db.Column(db.Integer, db.ForeignKey("Constellation.id"))
    constellation_desc = db.relationship("Constellation", backref="Planet")
    image = db.Column(db.Text())

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
