from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from inventory.models import Product

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Add Product')

    def validate_product_name(self, product_name):
        product = Product.query.filter_by(product_name=product_name.data).first()
        if product:
            raise ValidationError('That product is available. Please choose a different one.')
