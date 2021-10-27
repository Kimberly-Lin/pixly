import os

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, flash, redirect, render_template, request, jsonify
from uuid import uuid4
from PIL import Image
from PIL.ExifTags import TAGS
import boto3

# from models import db, connect_db, ModelName
from s3 import upload
from flask_cors import CORS
######################## AWS CONFIGURATION #########################
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_BUCKET = os.environ["AWS_BUCKET"]

s3 = boto3.resource('s3')
pixly_bucket = s3.Bucket(os.environ['AWS_BUCKET'])

######################## FLASK CONFIGURATION #########################
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
CORS(app)
# connect_db(app)

# debug = DebugToolbarExtension(app)
app.config['SECRET_KEY'] = 'secret'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# db.create_all()

############################## ROUTES ################################


@app.route("/upload", methods=['GET', 'POST'])
def upload_photo():
    """Shows photo upload form."""
    """Show upload form.
       Read & get metadata
       Save some portions of metadata to DB + caption
       Upload file to AWS
       Show success message"""
    breakpoint()
    img = request.files['file']
    print('img is', img)
    image = Image.open(img)
    print(image)
    print(img)
    # exifdata = image.getexif()
    # print('image', image)
    # print('exif', exifdata)
    # form = ImageForm()
    # if form.validate_on_submit():
    #     caption = form.caption.data
    #     image = form.image.data
    #     id = uuid4()
    #     breakpoint()
    #     image = Image.open(image.read())
    #     exifdata = image.getexif()
    #     for tag_id in exifdata:
    #         # get the tag name, instead of human unreadable tag id
    #         tag = TAGS.get(tag_id, tag_id)
    #         data = exifdata.get(tag_id)
    #         # decode bytes 
    #         if isinstance(data, bytes):
    #             data = data.decode()
    #         print(f"{tag:25}: {data}")
    #     breakpoint()
    #     resp = upload(image, id)
    #     print(resp)
        # aws_resp = upload_to_aws(image)
        # img_data = parse_image_data(image)
        # db_rep = upload_to_db(img_data, caption)
    return jsonify("hi")
