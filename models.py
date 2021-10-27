"""Models for pixly image app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class Image (db.Model):
    """Pets up for adoption"""

    __tablename__ = "images"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    name = db.Column(
        db.String(50),
        nullable=False)

    species = db.Column(
        db.String(50),
        nullable=False)

    photo_url = db.Column(
        db.String(5000), 
        nullable = False, 
        default = "") 

    age = db.Column(
        db.String(10),
        nullable=False)

    notes = db.Column(
            db.Text,
            nullable=True)

    available = db.Column(
            db.Boolean,
            nullable=False, 
            default=True)

                  
