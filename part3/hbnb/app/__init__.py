from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade

facade = HBnBFacade()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='2.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/docs')

    # Placeholder for API namespaces (endpoints will be added later)
    from .api.v1.users import api_usr
    from .api.v1.amenities import api_amnt
    from .api.v1.places import api_plc
    from .api.v1.reviews import api_rvw
    # Additional namespaces for places, reviews, and amenities will be added later
    api.add_namespace(api_usr, path='/api/v1/users')
    api.add_namespace(api_amnt, path='/api/v1/amenities')
    api.add_namespace(api_plc, path='/api/v1/places')
    api.add_namespace(api_rvw, path='/api/v1/reviews')

    return app