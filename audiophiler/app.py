from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import boto3
import host
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def test():
    return render_template("main.html")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        s3 = boto3.resource(service_name="s3", endpoint_url=host.s3_url)
        s3.Bucket("audiophiler").put_object(Key=secure_filename(f.filename), Body=f, ACL="public-read")
    return render_template("upload.html")


