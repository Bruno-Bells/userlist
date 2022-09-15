import datetime
from sqlalchemy import func, or_
from flask import abort
from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator

from lib.util_datetime import tzware_datetime
from project.extensions import db
from sqlalchemy import text, asc, desc, String


class ResourceMixin(object):
    # Keep track when records are created and updated.
    created_on = db.Column(db.DateTime(),
            default=tzware_datetime)
    updated_on = db.Column(db.DateTime(),
            default=tzware_datetime,
            onupdate=tzware_datetime)
    
    @classmethod
    def find_all(cls,):
        return cls.query.all()

    @classmethod
    def sort_by(cls, field, direction):
        """
        Validate the sort field and direction.

        :param field: Field name
        :type field: str
        :param direction: Direction
        :type direction: str
        :return: tuple
        """
        if field not in cls.__table__.columns:
            field = 'created_on'

        if direction not in ('asc', 'desc'):
            direction = 'asc'

        return field, direction



    @classmethod
    def bulk_query(cls, ids):
        """
        fectch more than 1 model instances.

        :param ids: List of ids to be fetched
        :type ids: list
        :return: List of model instances
        """
        if ids:
            return cls.query.filter(cls.id.in_(ids))

        return None


    @classmethod
    def group_and_count(cls, field):
        """
        Group results for a specific model and field.

        :param model: Name of the model
        :type model: SQLAlchemy model
        :param field: Name of the field to group on
        :type field: SQLAlchemy field
        :return: dict
        """
        count = func.count(field)
        query = db.session.query(count, field).group_by(field).all()

        return query


    def save_to_db(self):
        """
        Save a model instance.

        :return: None
        """
        db.session.add(self)
        db.session.commit()
        return None




    def __str__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)


    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id):
        rv = cls.get(id)
        if rv is None:
            abort(404)
        return rv

    def url(self):
        return f"/{self.__class__.__name__.lower()}/{self.id}"

    def to_dict(self):
        columns = self.__table__.columns.keys() + ["kind"]
        return {key: getattr(self, key, None) for key in columns}




