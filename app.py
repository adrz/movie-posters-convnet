from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS

from api.api import ApiPosters

appli = Flask(__name__)
CORS(appli)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(ApiPosters, '/v1/<id>')
appli.register_blueprint(api_bp)

if __name__ == "__main__":
    appli.run(debug=True)
