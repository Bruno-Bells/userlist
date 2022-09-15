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

    @app.route("/addData")
    def addData():
        fake = Faker()
        
        def _bulk_insert(model, data, label):
            """
            Bulk insert data to a specific model and log it. This is much more
            efficient than adding 1 row at a time in a loop.

            :param model: Model being affected
            :type model: SQLAlchemy
            :param data: Data to be saved
            :type data: list
            :param label: Label for the output
            :type label: str
            :param skip_delete: Optionally delete previous records
            :type skip_delete: bool
            :return: None
            """
            with app.app_context():
                # model.query.delete()

                db.session.commit()
                db.engine.execute(model.__table__.insert(), data)

                # _log_status(model.query.count(), label)

            return None

            """
        Generate fake users.
        """
        random_emails = []
        
        gender_options = ["male", "female", "unknown"]

        # click.echo("Working...")

        # Ensure we get about 100 unique random emails.
        for _ in range(0, 1000000):
            random_emails.append(fake.email())
            print("emails => ", _)

        random_emails = list(set(random_emails))

        chunks = [random_emails[x:x+100] for x in range(0, len(random_emails), 100)]

        for i in range(len(chunks)):
            chunks_emails = chunks[i]
            data = []
            while True:
                if len(chunks_emails) == 0:
                    break

                fake_datetime = fake.date_time_between(
                    start_date="-1y", end_date="now"
                ).strftime("%s")

                created_on = datetime.utcfromtimestamp(float(fake_datetime)).strftime(
                    "%Y-%m-%dT%H:%M:%S Z"
                )

                DOB_fake_datetime = fake.date_of_birth(minimum_age=0, maximum_age=115).strftime("%s")
                DOB = datetime.utcfromtimestamp(float(DOB_fake_datetime)).strftime(
                    "%Y-%m-%dT%H:%M:%S Z"
                )

                random_percent = random.random()

                if random_percent >= 0.9:
                    role = "is_superuser"
                if random_percent >= 0.7 and random_percent < 0.9:
                    role = "admin"
                else:
                    role = "member"

                email = chunks_emails.pop()

                random_percent = random.random()

                if random_percent >= 0.5:
                    random_trail = str(int(round((random.random() * 1000))))
                    username = fake.first_name() + random_trail
                else:
                    username = None

                fake_datetime = fake.date_time_between(
                    start_date="-1y", end_date="now"
                ).strftime("%s")

                current_sign_in_on = datetime.utcfromtimestamp(float(fake_datetime)).strftime(
                    "%Y-%m-%dT%H:%M:%S Z"
                )

                is_deleted_ = False if random.random()  >= 0.05 else True

                is_active_ = True if random.random()  >= 0.05 else False

                fname = fake.first_name()
                lname = fake.last_name()

                params = {
                    "created_on": created_on,
                    "updated_on": created_on,
                    "role": role,
                    "email": email,
                    "username": username,
                    "firstname": fname,
                    "lastname": lname,
                    'date_of_birth': DOB,
                    "password": UserModel.encrypt_password("password"),
                    "sign_in_count": random.random() * 100,
                    "current_sign_in_on": current_sign_in_on,
                    "current_sign_in_ip": fake.ipv4(),
                    "last_sign_in_on": current_sign_in_on,
                    "last_sign_in_ip": fake.ipv4(),
                    'is_deleted': is_deleted_,
                    'is_active': is_active_,
                    "phone_number": fake.phone_number(),
                    "gender": random.choice(gender_options),
                }
                print(len(data))
                data.append(params)

            _bulk_insert(UserModel, data, "users")
            # with open('tttt.txt', 'a') as f:
            #     f.write(f"added {i}")
        return jsonify({
                "message": "added"
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


