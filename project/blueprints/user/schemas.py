from marshmallow import Schema, fields
from project.extensions import ma
from project.blueprints.user.models import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("Password",)
        dump_only = ("id",)

