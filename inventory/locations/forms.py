from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LocationForm(FlaskForm):
    location_name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Add Location')
