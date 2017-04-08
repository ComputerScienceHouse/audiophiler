from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os, sys
import boto3
import tempfile
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


@app.route("/uploads/<path:filename>")
def get_file(filename):
    root_dir = os.path.dirname(os.getcwd())
    s3 = get_resource()
    s3.meta.client.download_file(BUCKET_NAME, filename, os.path.join(root_dir, "/temp/", filename))
    return send_from_directory(os.path.join(root_dir, "/temp/"), filename)


def get_resource():
    return boto3.resource(service_name="s3", endpoint_url=host.s3_url)


def get_bucket():
    return get_resource().Bucket(BUCKET_NAME)
