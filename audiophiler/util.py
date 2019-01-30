# File: util.py
# Audiophiler utility functions
# Credit to Liam Middlebrook and Ram Zallan
# https://github.com/liam-middlebrook/gallery

from functools import wraps
from flask import session

def audiophiler_auth(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uuid = str(session["userinfo"].get("sub", ""))
        uid = str(session["userinfo"].get("preferred_username", ""))
        auth_dict = {
            "uuid": uuid,
            "uid": uid
        }
        kwargs["auth_dict"] = auth_dict
        return func(*args, **kwargs)
    return wrapped_function
