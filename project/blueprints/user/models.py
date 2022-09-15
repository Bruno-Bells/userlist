from uuid import uuid4
from typing import Dict, List, Union
from sqlalchemy import or_
from lib.util_sqlalchemy import ResourceMixin
from project.extensions import db
from sqlalchemy_utils import UUIDType
from collections import OrderedDict
from werkzeug.security import generate_password_hash, check_password_hash

UserJSON = Dict[str, Union[int, str]]


# # User Model
class UserModel(ResourceMixin, db.Model):
    __tablename__ = "users"
    
    ROLE = OrderedDict(
        [
            ("member", "Member"), 
            ("admin", "Admin"), 
            ("is_superuser", "Is_Superuser")
        ]
    )
    GENDER = OrderedDict(
        [("male", "M"), ("female", "F"), ("unknown", "U"),]
    )

    __tablename__ = "users"
    Id = db.Column(UUIDType, unique=True, index=True, nullable=False, primary_key=True, default=uuid4)

    # personal details
    # # nullable=False, is used to cover up for required=True in our Schema
    firstname = db.Column(db.String(80), nullable=True)
    middlename = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=True)
    mobile = db.Column(db.Boolean, default=False, nullable=False)
    phone_number = db.Column(db.String(30), nullable=True, server_default="")
    gender  = db.Column(
        db.Enum(*GENDER, name="gender_types", native_enum=False),
        index=True,
        nullable=False,
        server_default="unknown",
    )
    date_of_birth = db.Column(db.DateTime(), nullable=True)

    # Authentication.
    role = db.Column(
        db.Enum(*ROLE, name="role_types", native_enum=False),
        index=True,
        nullable=False,
        server_default="member",
    )
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    username = db.Column(db.String(24), unique=True, index=True, nullable=True)
    email = db.Column(
        db.String(255), unique=True, index=True, nullable=True, server_default=""
    )
    password = db.Column(db.String(128), nullable=True, server_default="")

    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(db.DateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(db.DateTime())
    last_sign_in_ip = db.Column(db.String(45))
    


    def __str__(self,):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        return "username: {}, email: {}".format(self.Username, self.Email)

    @property
    def identity(self,):
        return (self.FirstName or self.Username or self.Email).capitalize()


    @classmethod
    def find_by_identity(cls, identity, fields=[]):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        # # taking not of logging attempts
        # current_app.logger.debug('{0} has tried to login'.format(identity))
        return cls.query.filter(
            (cls.Email == identity) | (cls.Phone == identity)
        ).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(Username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(Email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(Id=_id).first()
    
    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (cls.email.ilike(search_query),
                        cls.username.ilike(search_query))

        return or_(*search_chain)
    
    
