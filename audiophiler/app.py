from flask import Flask
from flask import render_template
from flask import request
from botocore.client import Config
from werkzeug.utils import secure_filename
import boto
import boto.s3.connection
import host         # host.py file containing s3 url


app = Flask(__name__)


BUCKET_NAME = "audiophiler"


@app.route("/", methods=["POST", "GET"])
def home():
    bucket = get_bucket()
    s3_files = bucket.list()
    return render_template("main.html", s3_files=s3_files, get_file=get_file)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        bucket = get_bucket()
        key = bucket.new_key(secure_filename(f.filename))
        key.set_contents_from_from_file(f)
    return render_template("upload.html")


def get_file(filename):
    bucket = get_bucket()
    key = bucket.get_key(filename)
    return key.generate_url(360, query_auth=True, force_http=True)


def get_bucket():
    return get_conn().get_bucket(BUCKET_NAME);


def get_conn():
    resource = boto.connect_s3(
                aws_access_key_id = host.key,
                aws_secret_access_key = host.secret,
                host = host.s3_url,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )
    return resource

