from PIL import Image
from PIL.ExifTags import TAGS


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
