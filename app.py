import os

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, flash, redirect, render_template, request
import boto3
# from models import db, connect_db, ModelName
from forms import ImageForm
from s3 import upload
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

    form = ImageForm()
    if form.validate_on_submit():
        caption = form.caption.data
        image = form.image.data
        print(image)
        print(caption)
        upload(image)
        breakpoint()
        # aws_resp = upload_to_aws(image)
        # img_data = parse_image_data(image)
        # db_rep = upload_to_db(img_data, caption)
        return redirect('/upload')
    else:
        return render_template("form.html", form=form)