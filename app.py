import boto3
import os

# from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from uuid import uuid4

from s3 import aws_upload, aws_upload_localfile
from models import db, connect_db, Image
from utils import getExif, edit, file_open, delete
######################## AWS CONFIGURATION #########################
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_BUCKET = os.environ["AWS_BUCKET"]

s3 = boto3.resource('s3')
pixly_bucket = s3.Bucket(os.environ['AWS_BUCKET'])

######################## FLASK CONFIGURATION #########################
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

# debug = DebugToolbarExtension(app)
app.config['SECRET_KEY'] = 'secret'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# db.drop_all()
db.create_all()

############################## ROUTES ################################

IMAGE_DB_COLUMNS = ["id", "title",
                    "file_extension", "width", "length", "img_url"]


@app.post("/upload")
def upload_image():
    """Shows image upload form."""

    imgStorage = request.files['file']
    title = request.form['title']
    extension = imgStorage.content_type.replace("image/", ".")
    id = str(uuid4())

    exif_decoded = getExif(imgStorage)

    # upload to AWS
    img_url = aws_upload(imgStorage, f"{id}{extension}")

    # upload to database
    dbImage = Image(
        id=id,
        title=title,
        file_extension=extension,
        width=exif_decoded.get("width"),
        length=exif_decoded.get("length"),
        img_url=img_url
    )

    db.session.add(dbImage)
    db.session.commit()

    imageDetails = {}
    for field in IMAGE_DB_COLUMNS:
        if (field == 'img_url'):
            imageDetails['imgUrl'] = dbImage.__getattribute__(field)
        else:
            imageDetails[field] = dbImage.__getattribute__(field)

    return jsonify(imageDetails)


@app.get("/all")
def get_all_images():
    """Fetch all images in the database.
    returns json of { images: [image,...] }"""

    result = Image.query.all()

    images = []
    for image in result:
        imageDetails = {}
        for field in IMAGE_DB_COLUMNS:
            if (field == 'img_url'):
                imageDetails['imgUrl'] = image.__getattribute__(field)
            else:
                imageDetails[field] = image.__getattribute__(field)
        images.insert(0,imageDetails)

    return jsonify({"images": images})


@app.get("/image/<id>")
def get_image(id):
    """Fetch single image from database by id, returns json of { image: {id, ...} }"""

    image = Image.query.get_or_404(id)
    imageDetails = {}
    for field in IMAGE_DB_COLUMNS:
        if (field == 'img_url'):
            imageDetails['imgUrl'] = image.__getattribute__(field)
        else:
            imageDetails[field] = image.__getattribute__(field)

    return jsonify({"image": imageDetails})


@app.post("/image/<id>/start_edit")
def start_edit(id):

    image = Image.query.get_or_404(id)
    file_location = file_open(image.img_url)

    return jsonify({"file_location": file_location})


@app.post("/image/<id>/edit")
def make_edit(id):
    req = request.get_json()
    file_location = req['file_location']
    edit_type = req['edit_type']
    print("edit_type", edit_type)
    edited_file = edit(file_location, edit_type)

    return jsonify({'file_location': file_location})


@app.post("/image/<id>/save_edits")
def save_edits(id):
    req = request.get_json()
    file_location = req['file_location']
    title = req['title']
    uuid = str(uuid4())
    aws_filename = uuid + '.jpeg'

    exif_decoded = getExif(file_location)
    # upload to AWS
    img_url = aws_upload_localfile(file_location, aws_filename)

    # upload to database
    dbImage = Image(
        id=uuid,
        title=title,
        file_extension='.jpeg',  # TODO: add conversion options
        width=exif_decoded.get("width"),
        length=exif_decoded.get("length"),
        img_url=img_url
    )

    db.session.add(dbImage)
    db.session.commit()

    image_details = {}
    for field in IMAGE_DB_COLUMNS:
        if (field == 'img_url'):
            image_details['imgUrl'] = dbImage.__getattribute__(field)
        else:
            image_details[field] = dbImage.__getattribute__(field)

    delete(file_location)

    return jsonify(image_details)


@app.route('/editimages/<path:path>')
def send_image(path):
    return send_from_directory("./tmp", path)

@app.after_request
def add_header(response):
    """Add non-caching headers on every request."""

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    response.cache_control.no_store = True
    return response
