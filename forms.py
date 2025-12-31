from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField

import app

class AddEventForm(FlaskForm):
    title = StringField('Title')
    date = DateField('Date')
    time = TimeField('Time')
    submit = SubmitField('Submit')

class UpdateEventForm(FlaskForm):
    title = StringField('Title')
    date = DateField('Date')
    time = TimeField('Time')
    submit = SubmitField('Submit')