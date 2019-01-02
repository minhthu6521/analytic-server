# -*- coding: utf-8 -*-
from flask import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EntityMixin(object):
    time_created = db.Column(db.DateTime)
    time_modified = db.Column(db.DateTime)


def json_property(name, column, default={}, docstring=None):
    """Facilitating json properties. NB, mutable argument `default` is ok here - never modified.
    Usage example:
    json_field, field = json_property('json_field', db.Column(MEDIUMTEXT), default={})
    Now `json_field` is column in the table, but almost always `field` should be used to access, modify, delete.
    """
    json_default = json.dumps(default)

    def getter(self):
        value = getattr(self, name, None)
        return json.loads(value if value else json_default)

    def setter(self, value):
        if value or (type(value) == type(default)):
            setattr(self, name, json.dumps(value))

    def deleter(self):
        setattr(self, name, None)

    return column, property(getter, setter, deleter, doc=docstring)