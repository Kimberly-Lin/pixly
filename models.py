"""Models for pixly image app."""

from flask_sqlalchemy import SQLAlchemy
# import enum

db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


# class MyEnum(enum.Enum):
#     jpeg = ".jpeg"
#     jpg = ".jpg"
#     png = ".png"


class Image (db.Model):
    """Images for pixly db"""

    __tablename__ = "images"

    def get(self, field):
        return self.__dict__[field]

    id = db.Column(
        db.String,
        primary_key=True)

    caption = db.Column(
        db.String(50),
        nullable=True,
        default="")

    # can try to figure out using enums later
    file_extension = db.Column(
        db.String(5),
        nullable=False)

    width = db.Column(
        db.Integer(),
        nullable=True)

    length = db.Column(
        db.Integer(),
        nullable=True)

    img_url = db.Column(
        db.Text,
        nullable=False)
