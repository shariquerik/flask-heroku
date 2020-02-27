from flask import (render_template, url_for, flash, redirect, request, Blueprint)
from inventory import db
from inventory.models import Product
from inventory.products.forms import ProductForm

products = Blueprint('products', __name__)

@products.route("/product/new", methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(product_name=form.product_name.data)
        db.session.add(product)
        db.session.commit()
        flash('Your product is successfully added in the product list!', 'success')
        return redirect(url_for('main.product'))
    return render_template('create.html', form=form, legend='New Product')


@products.route("/product/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm()
    if form.validate_on_submit():
        product.product_name = form.product_name.data
        db.session.commit()
        flash('Your product has been updated!', 'success')
        return redirect(url_for('main.product', product_id=product.product_id))
    elif request.method == 'GET':
        form.product_name.data = product.product_name
    form.submit.label.text = 'Update Product'
    return render_template('create.html', title='Update Product', form=form, legend='Update Product') 

@products.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', title='Update Product', product=product)


@products.route("/product/<int:product_id>/delete", methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Your product has been deleted!', 'success')
    return redirect(url_for('main.product'))



