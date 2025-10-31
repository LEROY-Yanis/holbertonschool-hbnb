from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade

facade = HBnBFacade()

def create_app():
    app = Flask(__name__)
    api = Api(app, version='2.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/docs')

    # Placeholder for API namespaces (endpoints will be added later)
    from .api.v1.users import api_usr
    from .api.v1.amenities import api_amnt
    from .api.v1.places import api_plc
    from .api.v1.reviews import api_rvw
    # Additional namespaces for places, reviews, and amenities will be added later

    return app