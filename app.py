import boto3
import os

# from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, jsonify, send_file
# flash, redirect, render_template,
from flask_cors import CORS
from uuid import uuid4

# from models import db, connect_db, ModelName
from s3 import aws_upload
from models import db, connect_db, Image
from utils import getExif, BW
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

IMAGE_DB_COLUMNS = ["id", "caption",
                    "file_extension", "width", "length", "img_url"]


@app.post("/upload")
def upload_image():
    """Shows image upload form."""

    imgStorage = request.files['file']
    caption = request.form['caption']
    extension = imgStorage.content_type.replace("image/", ".")
    id = str(uuid4())

    exif_decoded = getExif(imgStorage)

    # upload to AWS
    img_url = aws_upload(imgStorage, f"{id}{extension}")

    # upload to database
    dbImage = Image(
        id=id,
        caption=caption,
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
        images.append(imageDetails)

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
def edit(id):

    image = Image.query.get_or_404(id)
    edit_type = request.body["edit_type"]

    file_location = file_open(image.img_url)

    return send_file(f"./{result}")
