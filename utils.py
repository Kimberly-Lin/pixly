from PIL import Image
from PIL.ExifTags import TAGS

from uuid import uuid4

import requests
import os

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
    filename = str(uuid4())+'.jpeg'
    file_location = f"./temp_image_edits/{filename}"
    # open file from local
    file = open(file_location, "wb")
    file.write(image.content)
    file.close()

    return file_location


def edit(file_location, edit_type):
    """Take image at url and rotate 180 degrees"""
    # need to make folder where these images will live and figure out how to save to there
    # integrate pillow and save edited photo

    new_img = Image.open(file_location)
    
    if (edit_type == 'rotate'):
        new_img = new_img.rotate(90)
        new_img.save(file_location)

    if (edit_type == 'bw'):
        bw_img = new_img.convert('L')
        bw_img.save(file_location)

    return file_location


def delete(file_location):
    os.remove(file_location)
    return f"removed {file_location}"
    