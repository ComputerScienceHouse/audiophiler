# File: __init__.py
# Audiophiler main flask functions
# @author: Stephen Greene (sgreene570)


import hashlib
import os
from werkzeug.utils import secure_filename
from flask import Flask
from flask import render_template
from flask import request
from flask_pyoidc.flask_pyoidc import OIDCAuthentication


from audiophiler.s3 import get_file
from audiophiler.s3 import get_file_list
from audiophiler.s3 import get_date_modified
from audiophiler.s3 import get_bucket

from audiophiler.util import audiophiler_auth

app = Flask(__name__)
# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))


auth = OIDCAuthentication(app,
                          issuer = app.config["OIDC_ISSUER"],
                          client_registration_info = app.config["OIDC_CLIENT_CONFIG"])


# Get s3 bucket for use in functions and templates
s3_bucket = get_bucket(app.config["S3_URL"], app.config["S3_KEY"],
                app.config["S3_SECRET"], app.config["BUCKET_NAME"])


@app.route("/")
@auth.oidc_auth
@audiophiler_auth
def home():
    # Retrieve list of files for templating
    s3_files = get_file_list(s3_bucket)
    return render_template("main.html", s3_files=s3_files,
                get_file=get_file, get_date_modified=get_date_modified,
                s3_bucket=s3_bucket, auth_dict=auth_dict)


@app.route("/upload")
@auth.oidc_auth
@audiophiler_auth
def upload():
    if request.method == "POST":
        # Get file from upload form
        f = request.files["file"]
        # Sanitize file name
        filename = secure_filename(f.filename)
        # Iterate through file list and stop upload if file name already exists
        # TODO
        # Return error status to user
        for fname in get_file_list(BUCKET_NAME):
            if filename == fname.ke:
                # Return to refresh the upload page and stop the upload process
                return render_template("upload.html", auth_dict=auth_dict)
        # Hash the file contents (read file in ram)
        # File contents cannot be read in chunks (this is a flaw in boto file objects)
        file_hash = hashlib.md5(f.read()).hexdigest()
        # Reset file pointer to avoid EOF
        f.seek(0)
        # TODO
        # Check file hash against list of file hashes in db

        # Upload the file to the bucket
        upload_file(s3_bucket, filename, f)
    return render_template("upload.html", auth_dict=auth_dict)


@app.route("/logout")
@auth.oidc_logout
def logout():
    return redirect("/", 302)

