from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import send_from_directory
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


@app.route("/uploads/<path:filename>")
def get_file(filename):
    s3 = get_resource()
    s3_response = s3.Object(BUCKET_NAME, filename)
    return Response(s3_response.get()['Body'].read())


def get_resource():
    return boto3.resource(service_name="s3", endpoint_url=host.s3_url)


def get_bucket():
    return get_resource().Bucket(BUCKET_NAME)
