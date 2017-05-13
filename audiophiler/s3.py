# File: s3.py
# Audiophiler s3 API calls
# @author: Stephen Greene (sgreene570)


import boto
import boto.s3.connection
import creds            # Credentials fiel containing s3 keys and url


def get_file(bucket_name, file_name):
    bucket = get_bucket(bucket_name)
    key = bucket.get_key(filename)
    return key.generate_url(900, query_auth=True, force_http=True)

def get_file_list(bucket_name):
    bucket = get_bucket(bucket_name)
    return bucket.list()


def get_date_modified(filename):
    return get_bucket().get_key(filename).last_modified


def get_bucket(bucket_name):
    return get_resource().get_bucket(bucket_name);


def get_resource():
    resource = boto.connect_s3(
                aws_access_key_id = creds.key,
                aws_secret_access_key = creds.secret,
                host = creds.s3_url,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )
    return resource


