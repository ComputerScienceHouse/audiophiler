import os
import random
import string

# S3 config
S3_URL = os.getenv("S3_URL", default="s3.csh.rit.edu")
S3_KEY = os.getenv("S3_KEY", default=None)
S3_SECRET = os.getenv("S3_SECRET", default=None)
BUCKET_NAME = os.getenv("BUCKET_NAME", default="audiophiler")
SERVER_NAME = os.getenv("SERVER_NAME", default="audiophiler.csh.rit.edu")

# OpenID Connect SSO config
OIDC_ISSUER = os.getenv("OIDC_ISSUER", default="https://sso.csh.rit.edu/auth/realms/csh")
OIDC_CLIENT_CONFIG = {
    "client_id": os.getenv("OIDC_CLIENT_ID", default="audiophiler"),
    "client_secret": os.getenv("OIDC_CLIENT_SECRET", default=None),
    "post_logout_redirect_uris": [os.getenv("OIDC_LOGOUT_REDIRECT_URI", default="https://audiophiler.csh.rit.edu/logout")]
}
OIDC_REDIRECT_URI = os.getenv("OIDC_REDIRECT_URI", default="https://"+SERVER_NAME+"/redirect_uri")

# Git Hash
with open('commit.txt') as f: s = f.read()
GIT_REVISION = s

# Openshift secret
SECRET_KEY = os.getenv("SECRET_KEY", default=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64)))

# Database credentials
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", default=None)

PLUG_SUPPORT = os.environ.get('PLUG_ENABLED', False)

PAGE_SIZE = os.environ.get('PAGE_SIZE', 20)
