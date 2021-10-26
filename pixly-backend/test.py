import boto3
import os

s3 = boto3.resource('s3')
key_id = {"AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"]}
key = os.environ["AWS_SECRET_ACCESS_KEY"]

for bucket in s3.buckets.all():
    print(bucket.name)
