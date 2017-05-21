# File: __init__.py
# Audiophiler main flask functions
# @author: Stephen Greene (sgreene570)


import hashlib
import os
from werkzeug.utils import secure_filename
from flask import Flask
from flask import render_template
from flask import request


from audiophiler.s3 import get_file
from audiophiler.s3 import get_file_list
from audiophiler.s3 import get_date_modified
from audiophiler.s3 import get_bucket


app = Flask(__name__)
app.config.from_pyfile("config.py")

BUCKET_NAME = "audiophiler"


@app.route("/", methods=["POST", "GET"])
def home():
    bucket = get_bucket(BUCKET_NAME)
    s3_files = get_file_list(BUCKET_NAME)
    return render_template("main.html", s3_files=s3_files,
                get_file=get_file, get_date_modified=get_date_modified,
                bucket_name=BUCKET_NAME)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        # Get file from upload form
        f = request.files['file']
        # Sanitize file name
        filename = secure_filename(f.filename)
        # Break out of function if file already exists
        # TODO
        # Return error status to user
        for fname in get_file_list(BUCKET_NAME):
            if filename == fname.key:
                return render_template("upload.html")
        # Hash the file contents (read file in ram)
        file_hash = hashlib.md5(f.read()).hexdigest()
        # Reset file pointer to avoid EOF
        f.seek(0)
        # TODO
        # Check file hash against list of file hashes in db
        # Upload the file to the bucket
        bucket = get_bucket(BUCKET_NAME)
        key = bucket.new_key(filename)
        key.set_contents_from_file(f)
    return render_template("upload.html")
