import boto3
from botocore.exceptions import ClientError
from flask import Flask,redirect,jsonify
import logging
import os
from random import randint
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)

NUM_IMAGES = int(os.environ['NUM_IMAGES_IN_BUCKET']) # 4551
BUCKET_NAME = os.environ['BUCKET_NAME']

@app.route('/dne')
def gen_generated_image():
    image_num = randint(0, NUM_IMAGES)
    file_name = "samples/{:06d}.png".format(image_num)

    presigned_url = generate_presigned_url(BUCKET_NAME, file_name, 120)

    if presigned_url is not None:
        response = jsonify({'image_url': presigned_url})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        raise InternalServerError("s3 didn't produce a response")

def generate_presigned_url(bucket_name, object_name, expiration):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

@app.errorhandler(InternalServerError)
def handle_internal_error(e):
    return 'Internal Error. Check Logs or Try Again Later.\n', 500
