# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""All the database related entities are in this module."""

from . import db

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    path_to_image = db.Column(db.String(255), nullable=False)
    owner = db.Column(db.String(120), nullable=False)
    caption = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Image %r>' % self.name

# This is terrible design, we want to have subtables for each Image table 
# but for time's sake we decided one table of all comments would work
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_image = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    comment_string = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.author + self.parent_image


class Viewable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(120), nullable=False)
    user_name = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Viewable %r>' % self.image_name + user_name

