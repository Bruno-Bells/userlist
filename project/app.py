import os, random
from requests import request
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify
from marshmallow import ValidationError
from project.blueprints.user.views import user
from project.extensions import debug_toolbar, cors, ma, db, cache
from flask_swagger_ui import get_swaggerui_blueprint
from faker import Faker
from datetime import datetime
from project.blueprints.user.models import UserModel

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'
# API_URL = 'http://petstore.swagger.io/v2/swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "PowerToFly Users API"
    },
)

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    db.init_app(app)

    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    app.url_map.strict_slashes = False


    if settings_override:
        app.config.update(settings_override)
        
    @app.before_first_request
    def create_tables():
        db.create_all()
        
    # setting app level error handlers
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):  # except ValidationError as err
        return jsonify(err.messages), 400
    
    
    middleware(app)
    
    @app.route("/")
    def home():
        return jsonify({
                "message": "Welcome to WEB API!"
            }), 200

    app.register_blueprint(user, url_prefix="/user")
    
    error_templates(app)
    extensions(app)
    return app

def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    
    ma.init_app(app)
    # Using Redis Caching
    cache.init_app(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL' : 'redis://redis:6379/0', 'CACHE_REDIS_PORT': 6379, 'CACHE_REDIS_DB':0})
    debug_toolbar.init_app(app)
    cors.init_app(app, supports_credentials=True, origins="*")
    
    return None


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Swap request.remote_addr with the real IP address even if behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None


def error_templates(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        

        code = getattr(status, 'code', 500)
        
        res = {
            "responseCode": code,
            "responseDescription": getattr(status, 'name', ""),
            "responseMessage": getattr(status, 'description', "")
        }
        return res, code


    for error in [404, 429, 500]:
        app.errorhandler(error)(render_status)

    return None


