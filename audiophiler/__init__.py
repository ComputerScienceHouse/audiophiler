# File: __init__.py
# Audiophiler main flask functions
# @author: Stephen Greene (sgreene570)


import hashlib, os, flask_migrate, requests
from flask import Flask, render_template, request, jsonify
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


from audiophiler.s3 import get_file_s3, get_file_list, get_date_modified, get_bucket, upload_file
from audiophiler.util import audiophiler_auth


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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


# Database setup
db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)


# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()


# Import db models after instantiating db model
from audiophiler.models import File, Harold


@app.route("/")
@auth.oidc_auth
@audiophiler_auth
def home(auth_dict=None):
    # Retrieve list of files for templating
    db_files = File.query.all()
    return render_template("main.html", db_files=db_files,
                get_file_s3=get_file_s3, get_date_modified=get_date_modified,
                s3_bucket=s3_bucket, auth_dict=auth_dict)


@app.route("/upload", methods=["GET"])
@auth.oidc_auth
@audiophiler_auth
def upload_page(auth_dict=None):
    return render_template("upload.html", auth_dict=auth_dict)


@app.route("/upload", methods=["POST"])
@auth.oidc_auth
@audiophiler_auth
def upload(auth_dict=None):
    uploaded_files = [t[1] for t in request.files.items()]
    upload_status = {}
    upload_status["error"] = []
    upload_status["success"] = []

    for f in uploaded_files:
        # Sanitize file name
        filename = secure_filename(f.filename)

        # Hash the file contents (read file in ram)
        # File contents cannot be read in chunks (this is a flaw in boto file objects)
        file_hash = hashlib.md5(f.read()).hexdigest()
        # Reset file pointer to avoid EOF
        f.seek(0)

        # Check if file hash is the same as any files already in the db
        file_exists = False
        for db_file in File.query.all():
            if file_hash == db_file.file_hash:
                upload_status["error"].append(filename)
                file_exists = True
                break

        if file_exists:
            break

        # Add file info to db
        file_model = File(filename, auth_dict["uid"], file_hash)
        if file_model is None:
            upload_status["error"].append(filename)
            break

        # Upload file to s3
        upload_file(s3_bucket, file_hash, f)

        # Add file_model to DB and flush
        db.session.add(file_model)
        db.session.flush()
        db.session.commit()
        db.session.refresh(file_model)

        # Set success status info
        upload_status["success"].append(
            {
                "name": file_model.name,
                "file_hash": file_model.file_hash
            })

    return jsonify(upload_status)


@app.route("/logout")
@auth.oidc_logout
def logout():
    return redirect("/", 302)
