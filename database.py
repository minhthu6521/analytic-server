# -*- coding: utf-8 -*-
from flask import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EntityMixin(object):
    time_created = db.Column(db.DateTime)
    time_modified = db.Column(db.DateTime)