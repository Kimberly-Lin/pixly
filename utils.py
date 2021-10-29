from PIL import Image, ImageEnhance, ImageOps, ImageFilter
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
    # QUESTION: for kim, need to create temp_image_edits folder manually before this worked??
    file_location = "./temp_image_edits/" + filename
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

    # could add input for rotation angle
    if (edit_type == 'rotate'):
        new_img = new_img.rotate(90)
        new_img.save(file_location)

    if (edit_type == 'bw'):
        new_img = new_img.convert('L')
        new_img.save(file_location)

    # make 50% smaller
    if (edit_type == 'resize'):
        width, height = new_img.size
        new_img = new_img.resize(int(round(width/2)), int((round(height/2))))
        new_img.save(file_location)

    # flip left/right
    if (edit_type == 'side_flip'):
        new_img = new_img.transpose(Image.FLIP_LEFT_RIGHT)
        new_img.save(file_location)

    # flip top/bottom
    if (edit_type == 'top_flip'):
        new_img = new_img.transpose(Image.FLIP_TOP_BOTTOM)
        new_img.save(file_location)

    # color split and merge
    if (edit_type == 'color_split'):
        red, green, blue = new_img.split()
        new_img = Image.merge("RGB", (green, red, blue))
        new_img.save(file_location)

    # increase contrast by 1.5
    if (edit_type == 'contrast'):
        new_img = ImageEnhance.Contrast(new_img)
        new_img.enhance(1.5).save(file_location)

    # add black 30px border all around
    if (edit_type == 'border'):
        new_img = ImageOps.expand(
            new_img, border=(30, 30, 30, 30), fill="black")
        new_img.save(file_location)

    # add blur effect
    if (edit_type == 'blur'):
        new_img = new_img.filter(ImageFilter.GaussianBlur(5))
        new_img.save(file_location)

    return file_location


def delete(file_location):
    os.remove(file_location)
    return f"removed {file_location}"
