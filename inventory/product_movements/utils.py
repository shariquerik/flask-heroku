from flask import url_for, flash, redirect
from inventory.models import Product, Location, ProductMovement

#utils
def get_choices(form):
    location_choices = [(0, "---")]+[(location.location_id, location.location_name) for location in Location.query.all()]
    form.from_location.choices = location_choices
    form.to_location.choices = location_choices
    form.product_id.choices = [(product.product_id, product.product_name) for product in Product.query.all()]

def convert_location_id_to_name(id):
    if id: return Location.query.filter_by(location_id=id).first().location_name
    elif not id or id == 0: return ""

def convert_location_name_to_id(name):
    if name: return Location.query.filter_by(location_name=name).first().location_id
    else: return 0

def product_movement_exist(form, from_location, to_location):
    return ProductMovement.query.filter_by(from_location=from_location, to_location=to_location, product_id=form.product_id.data).first()

def error_conditions(form, from_location, to_location, existing_only_from_location, existing_only_to_location, check, qty):
    #Do not allow to create movement without location in either location field
    if from_location == "" and to_location == "":
        flash('Atleast one location is need', 'danger')
        return redirect(url_for('product_movements.new_product_movement'))
    
    #to location and from location cannot be same
    elif from_location == to_location:
        flash('Cannot transfer in same location, please select different location', 'danger')
        return redirect(url_for('product_movements.new_product_movement'))

    #check if from_location has enough quantity
    elif check == 'new' and existing_only_from_location and ((existing_only_from_location.qty - form.qty.data) < 0):
        flash('The quantity of product is not available in '+ from_location, 'danger')
        return redirect(url_for('product_movements.new_product_movement'))
    
    #check if from_location has enough quantity
    elif check == 'update' and existing_only_from_location and ((existing_only_from_location.qty - form.qty.data + qty) < 0):
        flash('The quantity of product is not available in '+ from_location, 'danger')
        return redirect(url_for('product_movements.new_product_movement'))

    #In from location product is not available so throw an error.
    elif (existing_only_to_location and (from_location != "" and to_location != "" and not existing_only_to_location) or to_location == "") and not existing_only_from_location:
        flash('The product is not available in '+ from_location +' location', 'danger')
        return redirect(url_for('product_movements.new_product_movement'))

    else:
        return 'No error'

