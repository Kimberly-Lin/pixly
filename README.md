# Pixly-Backend
Back-end for Pixly built in Python Flask, PostgreSQL, AWS S3, Pillow.

## Completed features
- AWS S3 integration to Flask
- Create db tables for images and AWS links
- Create utility functions for photo editing, image data parsing
- Create API routes for pixly front-end to call

## Getting Up & Running
1. Flask Environment Setup
    ```console
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt
    ```
2. Database Setup
    ```console
    (venv) $ psql
    =# CREATE DATABASE pixly;
    =# (control-d)
    ```
3. .env File Setup

    Add the following lines to your .env file:
    ```txt
    SECRET_KEY=some_key
    DATABASE_URL=postgresql:///pixly
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    AWS_BUCKET=your_aws_bucket_name
    ```
4. Run the Server
    ```console
    (venv) $ flask run
    ```
    
## More to-do:
- Build tagging system to images
- Create search function by tags or titles
- Implement tests
- Implement TypeScript to all front-end code

