import boto3
import os

# from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, flash, redirect, render_template, request, jsonify
from flask_cors import CORS
from uuid import uuid4

# from models import db, connect_db, ModelName
from s3 import aws_upload
from models import db, connect_db, DBImage
from utils import getExif
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
db.drop_all()
db.create_all()

############################## ROUTES ################################


@app.post("/upload")
def upload_photo():
    """Shows photo upload form."""

    imgStorage = request.files['file']
    caption = request.form['caption']
    extension = imgStorage.content_type.replace("image/", ".")
    id = uuid4()

    exif_decoded = getExif(imgStorage)

    #upload to AWS
    imgUrl = aws_upload(imgStorage, f"{id}{extension}")
    
    #upload to database
    dbImage = DBImage(
        id=id, 
        caption=caption, 
        file_extension=extension,
        width=exif_decoded.get("width"), 
        length=exif_decoded.get("length")
        )

    db.session.add(dbImage)
    db.session.commit()

    return jsonify({'imgUrl': imgUrl})
