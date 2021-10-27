import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_BUCKET = os.environ["AWS_BUCKET"]
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(AWS_BUCKET)

# data = open('./test1.jpg', 'rb')
# resp = pixly_bucket.put_object(Key='test1.jpg', Body=data)

def upload(image, id):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    # pixly_bucket = s3.Bucket(os.environ['AWS_BUCKET'])
    try:
        s3.upload_fileobj(
            image,
            AWS_BUCKET,
            id
        )
        
    except Exception as err:
        print("Something Happened: ", err)
        return err
    return "{}{}".format(S3_LOCATION, id)