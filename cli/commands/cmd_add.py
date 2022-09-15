import click
import random
from faker import Faker
from uuid import uuid4, uuid1
from time import time
from datetime import datetime
import numpy as np
from project.app import create_app
from project.extensions import db
from project.blueprints.user.models import UserModel
from sqlalchemy_utils import database_exists, create_database


# Create an app context for the database connection.
app = create_app()
db.app = app
db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
if not database_exists(db_uri):
    create_database(db_uri)
    
db.create_all()

fake = Faker()
bool_options = [True, False]
gender_options = ["male", "female", "unknown"]

INITIAL_SEED_COUNT = app.config["INITIAL_SEED_COUNT"]

def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo("Created {0} {1}".format(count, model_label))

    return None

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
        model.query.delete()

        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None

@click.group()
def cli():
    """ Add items to the database. """
    pass


@click.command()
def users():
    """
    Generate fake users.
    """
    random_emails = []
    data = []

    click.echo("Working...")

    # Ensure we get about 100 unique random emails.
    for _ in range(0, INITIAL_SEED_COUNT):
        random_emails.append(fake.email())
        print("emails => ", _)

    random_emails = list(set(random_emails))


    while True:
        if len(random_emails) == 0:
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

        email = random_emails.pop()

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

    return _bulk_insert(UserModel, data, "users")



@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(users)

    return None


cli.add_command(users)
cli.add_command(all)


