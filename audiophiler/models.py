# File: models.py
# Audiophiler sqlalchemy database models
# @author Stephen Greene (sgreene570)


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text


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

