# File: util.py
# Audiophiler utility functions
# Credit to Liam Middlebrook and Ram Zallan
# https://github.com/liam-middlebrook/gallery

from functools import wraps
from flask import session
from audiophiler.models import Tour

def audiophiler_auth(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uuid = str(session["userinfo"].get("sub", ""))
        uid = str(session["userinfo"].get("preferred_username", ""))
        groups = str(session["groups"].get("groups", []))
        print(session)
        auth_dict = {
            "uuid": uuid,
            "uid": uid,
            "groups": groups,
        }
        kwargs["auth_dict"] = auth_dict
        return func(*args, **kwargs)
    return wrapped_function

def get_tour_lock_status():
    lock = Tour.query.first()
    return lock.tour_lock
