from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import boto
import boto.s3.connection
import creds             # credentials file containg s3 keys and url


app = Flask(__name__)


BUCKET_NAME = "audiophiler"


@app.route("/", methods=["POST", "GET"])
def home():
    bucket = get_bucket()
    s3_files = bucket.list()
    return render_template("main.html", s3_files=s3_files,
                get_file=get_file, get_date_modified=get_date_modified)


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
    return key.generate_url(900, query_auth=True, force_http=True)


def get_date_modified(filename):
    return get_bucket().get_key(filename).last_modified


def get_bucket():
    return get_conn().get_bucket(BUCKET_NAME);


def get_conn():
    resource = boto.connect_s3(
                aws_access_key_id = creds.key,
                aws_secret_access_key = creds.secret,
                host = creds.s3_url,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )
    return resource
