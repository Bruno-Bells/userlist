from flask import Blueprint
from flask_restful import Api
from project.blueprints.user.resources import UsersList


user = Blueprint(
    "user", 
    __name__
)

api = Api(user)


api.add_resource(UsersList, "", endpoint="user")
