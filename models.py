from flask_sqlalchemy import SQLAlchemy

# This is the connection to the database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)

class Pet(db.Model):

    __tablename__ = "pet"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text,nullable=False, unique=True)

    species = db.Column(db.Text,nullable=False,unique=False)

    photo_url = db.Column(db.String(300),nullable=True,unique=False)

    age = db.Column(db.Integer,nullable=True)

    notes = db.Column(db.Text,nullable=True,unique=False)

    available = db.Column(db.Boolean,default=False,nullable=True)