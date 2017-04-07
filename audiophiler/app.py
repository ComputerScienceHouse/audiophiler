from flask import Flask
from flask import render_template
import boto3
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def test():
    return render_template("main.html")


def main():
    #s3 = boto3.resource(service_name="s3", endpoint_url=host.s3_url)
    #data = open("test.mp3", "rb")
    #s3.Bucket("audiophiler").put_object(Key="testsong.mp3", Body=data, ACL="public-read")
    return

if __name__ == "__main__":
    main()
