from flask import (render_template, url_for, flash, redirect, request, Blueprint)
from inventory import db
from inventory.models import Location
from inventory.locations.forms import LocationForm

locations = Blueprint('locations', __name__)

@locations.route("/location/new", methods=['GET', 'POST'])
def new_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(location_name=form.location_name.data)
        db.session.add(location)
        db.session.commit()
        flash('Your location is successfully added in the location list!', 'success')
        return redirect(url_for('main.location'))
    return render_template('create.html', form=form, legend='New Location')


@locations.route("/location/<int:location_id>/update", methods=['GET', 'POST'])
def update_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm()
    if form.validate_on_submit():
        location.location_name = form.location_name.data
        db.session.commit()
        flash('Your location has been updated!', 'success')
        return redirect(url_for('main.location', location_id=location.location_id))
    elif request.method == 'GET':
        form.location_name.data = location.location_name
    form.submit.label.text = 'Update Location'
    return render_template('create.html', title='Update Location', form=form, legend='Update Location') 

@locations.route("/location/<int:location_id>")
def location(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('location.html', title='Update Location', location=location)


@locations.route("/location/<int:location_id>/delete", methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Your location has been deleted!', 'success')
    return redirect(url_for('main.location'))


