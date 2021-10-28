from PIL import Image
from PIL.ExifTags import TAGS

from uuid import uuid4

import requests


def getExif(imgFileStorage):
    """From image, return exif data as a dictionary"""

    image = Image.open(imgFileStorage)
    exifdata = image.getexif()
    exif_decoded = {}
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        if tag == 'TileWidth' or tag == 'ImageWidth':
            exif_decoded['width'] = data
        elif tag == 'TileLength' or tag == 'ImageLength':
            exif_decoded['length'] = data
        else:
            exif_decoded[tag] = data

    return exif_decoded


def file_open(img_url):
    image = requests.get(img_url)

    # open file from local
    file = open("temp.jpg", "wb")
    file.write(image.content)
    file.close()

    return "temp.jpg"


def edit("temp.jpg", edit_type):
    """Take image at url and rotate 180 degrees"""
    # need to make folder where these images will live and figure out how to save to there
    # integrate pillow and save edited photo

    new_img = Image.open("temp.jpg")

    if (rotate):
        new_img = new_img.rotate(180)
    if (bw):
    new_img.save("./temp_rotated.jpg")
    # Saved in the same relative location
    # file.save("rotated_picture.jpg")
    return "temp_rotated.jpg"
