# File: __init__.py
# Audiophiler main flask functions
# @author: Stephen Greene (sgreene570)


import hashlib, os, flask_migrate, requests, subprocess, random, json
from flask import Flask, render_template, request, jsonify, redirect
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from csh_ldap import CSHLDAP


from audiophiler.s3 import get_file_s3, get_file_list, get_date_modified, get_bucket, upload_file
from audiophiler.util import audiophiler_auth


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))


app.config["GIT_REVISION"] = subprocess.check_output(['git',
                                                      'rev-parse',
                                                      '--short',
                                                      'HEAD']).decode('utf-8').rstrip()


auth = OIDCAuthentication(app,
                          issuer = app.config["OIDC_ISSUER"],
                          client_registration_info = app.config["OIDC_CLIENT_CONFIG"])


# Get s3 bucket for use in functions and templates
s3_bucket = get_bucket(app.config["S3_URL"], app.config["S3_KEY"],
                app.config["S3_SECRET"], app.config["BUCKET_NAME"])


# Database setup
db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

ldap = CSHLDAP(app.config["LDAP_BIND_DN"],
               app.config["LDAP_BIND_PW"])


# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings()


# Import db models after instantiating db model
from audiophiler.models import File, Harold, Auth


@app.route("/")
@auth.oidc_auth
@audiophiler_auth
def home(auth_dict=None):
    # Retrieve list of files for templating
    db_files = File.query.all()
    harolds = get_harold_list(auth_dict["uid"])
    is_rtp = ldap_is_rtp(auth_dict["uid"])
    is_eboard = ldap_is_eboard(auth_dict["uid"])
    return render_template("main.html", db_files=db_files,
                get_date_modified=get_date_modified, s3_bucket=s3_bucket,
                auth_dict=auth_dict, harolds=harolds, is_rtp=is_rtp,
                is_eboard=is_eboard)


@app.route("/mine")
@auth.oidc_auth
@audiophiler_auth
def mine(auth_dict=None):
    # Retrieve list of files for templating
    db_files = File.query.filter_by(author=auth_dict["uid"]).all()
    harolds = get_harold_list(auth_dict["uid"])
    return render_template("main.html", db_files=db_files,
                get_file_s3=get_file_s3, get_date_modified=get_date_modified,
                s3_bucket=s3_bucket, auth_dict=auth_dict, harolds=harolds,
                is_rtp=False, is_eboard=False)


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


@app.route("/delete/<string:file_hash>", methods=["POST"])
@auth.oidc_auth
@audiophiler_auth
def delete_file(file_hash, auth_dict=None):
    file_model = File.query.filter(File.file_hash == file_hash).first()

    if file_model is None:
        return "File Not Found", 404

    if not auth_dict["uid"] == file_model.author:
        if not (ldap_is_eboard(auth_dict["uid"]) or ldap_is_rtp(auth_dict["uid"])):
            return "Permission Denied", 403

    db.session.delete(file_model)
    db.session.flush()
    db.session.commit()
    remove_harold(file_hash, auth_dict)

    return "OK go for it", 200


@app.route("/get_file_url/<string:file_hash>")
@auth.oidc_auth
@audiophiler_auth
def get_s3_url(file_hash, auth_dict=None):
    # Endpoint to return a presigned url to the s3 asset
    return redirect(get_file_s3(s3_bucket, file_hash))


@app.route("/set_harold/<string:file_hash>", methods=["POST"])
@auth.oidc_auth
@audiophiler_auth
def set_harold(file_hash, auth_dict=None):
    harold_model = Harold(file_hash, auth_dict["uid"])
    db.session.add(harold_model)
    db.session.flush()
    db.session.commit()
    db.session.refresh(harold_model)
    return "OK", 200


@app.route("/delete_harold/<string:file_hash>", methods=["POST"])
@auth.oidc_auth
@audiophiler_auth
def remove_harold(file_hash, auth_dict=None):
    harold_model = Harold.query.filter(Harold.file_hash == file_hash).first()
    if harold_model is None:
        return "File Not Found", 404

    db.session.delete(harold_model)
    db.session.flush()
    db.session.commit()

    return "OK go for it", 200


@app.route("/get_harold/<string:uid>", methods=["POST"])
def get_harold(uid, auth_dict=None):
    data_dict = request.get_json()
    if data_dict["auth_key"]:
        auth_models = Auth.query.all()
        for auth in auth_models:
            if auth.auth_key == data_dict["auth_key"]:
                harolds = get_harold_list(uid)
                return get_file_s3(s3_bucket, random.choice(harolds))

    return "Permission denied", 403


@app.route("/logout")
@auth.oidc_logout
def logout():
    return redirect("/", 302)


def get_harold_list(uid):
    harold_list = Harold.query.all()
    harolds = []
    for harold in harold_list:
        if harold.owner == uid:
            harolds.append(harold.file_hash)

    return harolds


def ldap_is_eboard(uid):
    eboard_group = ldap.get_group("eboard")
    return eboard_group.check_member(ldap.get_member(uid, uid=True))


def ldap_is_rtp(uid):
    rtp_group = ldap.get_group("rtp")
    return rtp_group.check_member(ldap.get_member(uid, uid=True))


