# File: s3.py
# Audiophiler s3 API calls
# @author: Stephen Greene (sgreene570)


import boto
import boto.s3.connection
import audiophiler.creds


def get_file(bucket_name, filename):
    bucket = get_bucket(bucket_name)
    key = bucket.get_key(filename)
    # Generates presigned URL that lasts for 900 seconds (15 minutes)
    # If streaming begins prior to the time cutoff, s3 will allow
    # for the streaming to continue, uninterrupted.
    return key.generate_url(900, query_auth=True, force_http=True)


def get_file_list(bucket_name):
    bucket = get_bucket(bucket_name)
    return bucket.list()


def get_date_modified(bucket_name, filename):
    return get_bucket(bucket_name).get_key(filename).last_modified


def get_bucket(bucket_name):
    return get_resource().get_bucket(bucket_name);


def get_resource():
    resource = boto.connect_s3(
                aws_access_key_id = audiophiler.creds.key,
                aws_secret_access_key = audiophiler.creds.secret,
                host = audiophiler.creds.s3_url,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )
    return resource
