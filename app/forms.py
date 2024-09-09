from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms_alchemy import QuerySelectField, QuerySelectMultipleField
from app.models import Constellation, Lifecycle


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=51)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5,max=51)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Add_Star(FlaskForm):
    def choice_constellation():
        return Constellation.query

    def choice_stage():
        return Lifecycle.query
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    constellation = QuerySelectField(query_factory=choice_constellation, allow_blank=True)
    image = FileField('Image')
    stage = QuerySelectField(query_factory=choice_stage)
    submit = SubmitField('Submit')


class Add_Constellation(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    story = TextAreaField('Story / Myth')
    image = FileField('Image')
    months = QuerySelectMultipleField('Months Viewable')
    submit = SubmitField('Submit')
