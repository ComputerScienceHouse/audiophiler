#!./audiophiler/bin/python

from flask import Flask
import boto3
import botocore
import host


@app.route("/upload", methods=["POST"])
def upload():


def main():
    s3 = boto3.resource(service_name="s3", endpoint_url=host.s3_url)
    data = open("test.mp3", "rb")
    s3.Bucket("audiophiler").put_object(Key="testsong.mp3", Body=data, ACL="public-read")


if __name__ == "__main__":
    main()
