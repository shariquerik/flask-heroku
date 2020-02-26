from flask import render_template, request, Blueprint
from inventory.models import Product, Location, ProductMovement
from inventory import db

main = Blueprint('main', __name__)

#inventory
@main.route("/")
@main.route("/product")
def product():
    products = Product.query.order_by(Product.product_name).all()
    return render_template('product.html', title='Product',products=products)

@main.route("/location")
def location():
    locations = Location.query.order_by(Location.location_name).all()
    return render_template('location.html', title='Location',locations=locations)

@main.route("/product_movement")
def product_movement():
    product_movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    products = Product.query
    return render_template('product_movement.html', title='Moved Product',product_movements=product_movements, products=products)


@main.route("/report")
def report():
    product_movements = db.session.query(ProductMovement.to_location, ProductMovement.product_id).filter(ProductMovement.from_location=="").distinct(ProductMovement.to_location).all()
    product = Product.query
    qty = ProductMovement.query
    return render_template('report.html', title='Report', product_movements=product_movements, qty=qty, product=product)

@main.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')