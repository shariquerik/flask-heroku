from datetime import datetime
from inventory import db

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Product('{self.product_name}')"

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Location('{self.location_name}')"

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    from_location = db.Column(db.String(20), db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String(20), db.ForeignKey('location.location_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ProductMovement( '{self.timestamp}', '{self.from_location}', '{self.to_location}', '{self.product_id}', '{self.qty}')"