# File: s3.py
# Audiophiler s3 API calls
# @author: Stephen Greene (sgreene570)


import boto
import boto.s3.connection


def get_file_s3(bucket, filename):
    key = bucket.get_key(filename)
    # Generates presigned URL that lasts for 900 seconds (15 minutes)
    # If streaming begins prior to the time cutoff, s3 will allow
    # for the streaming to continue, uninterrupted.
    return key.generate_url(900, query_auth=True, force_http=True)


def get_file_list(bucket):
    # List all files in the bucket
    return bucket.list()


def get_date_modified(bucket, filename):
    # Get date modified for a specific file in the bucket
    return bucket.get_key(filename).last_modified


def upload_file(bucket, filename, f):
    # Create bucket key with filename
    key = bucket.new_key(filename)
    # Upload the file
    key.set_contents_from_file(f)


def remove_file(bucket, filename):
    bucket.delete_key(filename)


def get_bucket(s3_url, s3_key, s3_secret, bucket_name):
    # Establish s3 connection through boto
    conn = boto.connect_s3(
                aws_access_key_id = s3_key,
                aws_secret_access_key = s3_secret,
                host = s3_url,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )
    # Return the bucket rather than the entire resource
    return conn.get_bucket(bucket_name)
