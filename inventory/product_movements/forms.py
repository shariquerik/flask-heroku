from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class ProductMovementForm(FlaskForm):
    from_location = SelectField(u'From', coerce=int)
    to_location = SelectField(u'To', coerce=int)
    product_id = SelectField('Product Name', coerce=int, validators=[DataRequired()])
    qty = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Move Product')