from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_caching import Cache

cache = Cache()
debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()




