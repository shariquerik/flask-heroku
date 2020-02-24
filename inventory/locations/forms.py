from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from inventory.models import Location

class LocationForm(FlaskForm):
    location_name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Add Location')

    def validate_location_name(self, location_name):
        location = Location.query.filter_by(location_name=location_name.data).first()
        if location:
            raise ValidationError('That location is available. Please choose a different one.')
