import os
S3_URL = os.getenv("S3_URL", default="s3.csh.rit.edu")
S3_KEY = os.getenv("S3_KEY", default=None)
S3_SECRET = os.getenv("S3_SECRET", default=None)
BUCKET_NAME = os.getenv("BUCKET_NAME", default="audiophiler")
SERVER_NAME = os.getenv("SERVER_NAME", default="audiophiler.csh.rit.edu")

# OpenID Connect SSO config
OIDC_ISSUER = os.getenv("OIDC_ISSUER", default="https://sso.csh.rit.edu/realms/csh")
OIDC_CLIENT_CONFIG = {
    "client_id": os.getenv("OIDC_CLIENT_ID", default="audiophiler"),
    "client_secret": os.getenv("OIDC_CLIENT_SECRET", default=None),
    "post_logout_redirect_uris": [os.getenv("OIDC_LOGOUT_REDIRECT_URI", default="https://audiophiler.csh.rit.edu/logout")]
}
