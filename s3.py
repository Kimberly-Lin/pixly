import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_BUCKET = os.environ["AWS_BUCKET"]
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(AWS_BUCKET)


def aws_upload(image, filename):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        image.seek(0)
        s3.upload_fileobj(
            image,
            AWS_BUCKET,
            filename,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': image.content_type
            }
        )
    except Exception as err:
        print("Something Happened: ", err)
        return err

    return "{}{}".format(S3_LOCATION, filename)


def aws_upload_localfile(filename, object_name=None):
    """Upload a file to an S3 bucket

    :param filename: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then filename is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use filename
    if object_name is None:
        object_name = os.path.basename(filename)
    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        s3_client.upload_file(
            filename,
            AWS_BUCKET,
            object_name,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': 'image/jpeg'
            })
    except ClientError as e:
        print(e)
        return False
    return "{}{}".format(S3_LOCATION, object_name)
