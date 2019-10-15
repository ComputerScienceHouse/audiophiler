# File: models.py
# Audiophiler sqlalchemy database models

from sqlalchemy import Column, Integer, Text, Boolean

from audiophiler import db

class File(db.Model):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    file_hash = Column(Text, nullable=False)

    def __init__(self, name, author, file_hash):
        self.name = name
        self.author = author
        self.file_hash = file_hash

class Harold(db.Model):
    __tablename__ = "harolds"
    id = Column(Integer, primary_key=True)
    file_hash = Column(Text, nullable=False)
    owner = Column(Text, nullable=False)

    def __init__(self, file_hash, owner):
        self.file_hash = file_hash
        self.owner = owner

class Auth(db.Model):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True)
    auth_key = Column(Text, nullable=False)

    def __init__(self, auth_key):
        self.auth_key = auth_key

class Tour(db.Model):
    __tablename__ = "tour"
    tour_lock = Column(Boolean, primary_key=True, default=False)
