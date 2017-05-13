# File: __init__.py
# Audiophiler main flask functions
# @author: Stephen Greene (sgreene57)


from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import hashlib
import s3       #s3.py file for s3 API calls


app = Flask(__name__)


BUCKET_NAME = "audiophiler"


@app.route("/", methods=["POST", "GET"])
def home():
    bucket = get_bucket(bucket_name)
    s3_files = get_file_list(bucket_name)
    return render_template("main.html", s3_files=s3_files,
                get_file=get_file, get_date_modified=get_date_modified)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        # Get file from upload form
        f = request.files['file']
        # Sanitize file name
        filename = secure_filename(f.filename)
        # Hash the file contents
        file_hash = hashlib.md5(f.read()).hexdigest()
        f.seek(0) # Reset file pointer to avoid EOF
        # Check file hash against list of file hashes in db
        # Upload the file tot he bucket
        bucket = get_bucket(BUCKET_NAME)
        key = bucket.new_key(filename)
        key.set_contents_from_file(f)
    return render_template("upload.html")
