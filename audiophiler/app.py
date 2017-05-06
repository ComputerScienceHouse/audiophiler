from flask import Flask
from flask import render_template
from flask import request
from botocore.client import Config
from werkzeug.utils import secure_filename
import boto3
import host         # host.py file containing s3 url


app = Flask(__name__)


BUCKET_NAME = "audiophiler"


@app.route("/", methods=["POST", "GET"])
def home():
    s3 = get_resource()
    bucket = get_bucket()
    s3_files = bucket.objects.all()
    return render_template("main.html", s3_files=s3_files, get_file=get_file)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        bucket = get_bucket()
        bucket.put_object(Key=secure_filename(f.filename), Body=f)
    return render_template("upload.html")


def get_file(filename):
    s3_client = get_resource().meta.client
    return s3_client.generate_presigned_url("get_object", Params = {"Bucket" : BUCKET_NAME, "Key" : filename}, ExpiresIn = 100)


def get_bucket():
    return get_resource().Bucket(BUCKET_NAME)


def get_resource():
    return boto3.resource(service_name="s3", endpoint_url=host.s3_url,
        config=Config(signature_version="s3v4"))

