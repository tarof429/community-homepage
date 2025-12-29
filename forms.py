from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

import app

class AddEventForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Submit')

class UpdateEventForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Submit')