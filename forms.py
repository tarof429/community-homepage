from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField

import app

class AddEventForm(FlaskForm):
    title = StringField('Title')
    date = DateField('Date')
    submit = SubmitField('Submit')

class UpdateEventForm(FlaskForm):
    title = StringField('Title')
    date = DateField('Date')
    submit = SubmitField('Submit')