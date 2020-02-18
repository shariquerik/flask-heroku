from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from inventory.config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from inventory.products.routes import products
    from inventory.locations.routes import locations
    from inventory.product_movements.routes import product_movements
    from inventory.main.routes import main
    from inventory.errors.handlers import errors
    app.register_blueprint(products)
    app.register_blueprint(locations)
    app.register_blueprint(product_movements)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app