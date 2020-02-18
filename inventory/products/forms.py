from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Add Product')
