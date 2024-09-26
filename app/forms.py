from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileAllowed
from wtforms_alchemy import QuerySelectField, QuerySelectMultipleField
from app.models import Constellation, Lifecycle

# Constants
MIN_USR = 3
MIN_PASSWORD = 5
MAX = 50


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=MIN_USR, max=MAX)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=MIN_PASSWORD, max=MAX)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords must match'),
                                                 Length(min=MIN_PASSWORD, max=MAX)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=MIN_USR, max=MAX)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=MIN_PASSWORD, max=MAX)])
    submit = SubmitField('Submit')


class Add_Star(FlaskForm):

    def choice_constellation():
        return Constellation.query

    def choice_stage():
        return Lifecycle.query

    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    constellation = QuerySelectField(query_factory=choice_constellation,
                                     allow_blank=True)
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                       'Images only!')])
    stage = QuerySelectField(query_factory=choice_stage)
    submit = SubmitField('Add')


class Add_Constellation(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    story = TextAreaField('Story / Myth')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                       'Images only!')])
    months = QuerySelectMultipleField('Months Viewable')
    submit = SubmitField('Add')
