from flask import render_template, url_for, flash, redirect, request, Blueprint
from inventory import db
from inventory.models import Product, Location, ProductMovement
from inventory.product_movements.forms import ProductMovementForm
from inventory.product_movements.utils import get_choices, convert_location_id_to_name, product_movement_exist, error_conditions

product_movements = Blueprint('product_movements', __name__)

@product_movements.route("/product_movement/new", methods=['GET', 'POST'])
def new_product_movement():
    form = ProductMovementForm()

    get_choices(form)

    from_location = convert_location_id_to_name(form.from_location.data)
    to_location = convert_location_id_to_name(form.to_location.data)
    
    existing_product_movement = product_movement_exist(form, from_location, to_location)
    existing_only_from_location = product_movement_exist(form, "", from_location)
    existing_only_to_location = product_movement_exist(form, "", to_location)
    
    if form.validate_on_submit():
        error = error_conditions(form, from_location, to_location, existing_only_from_location, existing_only_to_location)
        if(error == 'No error'):
            #qty++ in to_location
            if existing_product_movement and existing_product_movement.from_location == "" and existing_product_movement.to_location != "":
                existing_only_to_location.qty = existing_only_to_location.qty + form.qty.data

            #qty-- in from_location
            elif existing_product_movement and existing_product_movement.from_location != "" and existing_product_movement.to_location == "":
                existing_only_from_location.qty = existing_only_from_location.qty - form.qty.data

            #qty++ in to_location and qty-- in from_location
            elif (existing_product_movement and existing_product_movement.from_location != "" and existing_product_movement.to_location != "") or (existing_only_to_location and existing_only_from_location):
                existing_only_to_location.qty = existing_only_to_location.qty + form.qty.data
                existing_only_from_location.qty = existing_only_from_location.qty - form.qty.data

            #decrement from from_location and then create to location
            elif existing_only_from_location and not existing_only_to_location:
                existing_only_from_location.qty = existing_only_from_location.qty - form.qty.data
                if to_location != "":
                    product_to = ProductMovement(from_location="", to_location=to_location, product_id=form.product_id.data, qty=form.qty.data)
                    db.session.add(product_to)
                    db.session.commit()

            #Do Nothing
            else:
                pass

            product_movement = ProductMovement(from_location=from_location, to_location=to_location, product_id=form.product_id.data, qty=form.qty.data)
            db.session.add(product_movement)
            db.session.commit()
            flash('Your product movement is successfully added in the product movement list!', 'success')
            return redirect(url_for('main.product_movement'))
    return render_template('create.html', form=form, legend='New Product Movement')


@product_movements.route("/product_movement/<int:movement_id>/update", methods=['GET', 'POST'])
def update_product_movement(movement_id):
    product_movement = ProductMovement.query.get_or_404(movement_id)
    form = ProductMovementForm()
    location_choices = [(0, "---")]+[(location.location_id, location.location_name) for location in Location.query.all()]
    form.from_location.choices = location_choices
    form.to_location.choices = location_choices
    form.product_id.choices = [(product.product_id, product.product_name) for product in Product.query.all()]

    if form.validate_on_submit():
        if form.from_location.data != 0:
            product_movement.from_location = Location.query.filter_by(location_id=form.from_location.data).first().location_name
        else:
            product_movement.from_location = ""

        if form.to_location.data != 0:
            product_movement.to_location = Location.query.filter_by(location_id=form.to_location.data).first().location_name
        else:
            product_movement.to_location = ""
        product_movement.product_id = form.product_id.data
        product_movement.qty = form.qty.data
        db.session.commit()
        flash('Your product movement has been updated!', 'success')
        return redirect(url_for('product_movements.product_movement', movement_id=product_movement.movement_id))
    elif request.method == 'GET':
        if product_movement.from_location != "":
            form.from_location.data = Location.query.filter_by(location_name=product_movement.from_location).first().location_id
        else:
            form.from_location.data = 0

        if product_movement.to_location != "":
            form.to_location.data = Location.query.filter_by(location_name=product_movement.to_location).first().location_id
        else:
            form.to_location.data = 0
        form.product_id.data = product_movement.product_id
        form.qty.data = product_movement.qty
    return render_template('create.html', title='Update Moved Product', form=form, legend='Update Moved Product') 

@product_movements.route("/product_movement/<int:movement_id>")
def product_movement(movement_id):
    product_movement = ProductMovement.query.get_or_404(movement_id)
    products = Product.query
    return render_template('product_movement.html', title='Update Moved Product', product_movement=product_movement, products=products)


@product_movements.route("/product_movement/<int:movement_id>/delete", methods=['POST'])
def delete_product_movement(movement_id):
    product_movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(product_movement)
    db.session.commit()
    flash('Your product movement has been deleted!', 'success')
    return redirect(url_for('main.product_movement'))


