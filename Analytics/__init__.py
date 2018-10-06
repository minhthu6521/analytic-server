# -*- coding: utf-8 -*-

from flask import Flask
from flask_caching import Cache
from blueprint import bp
import Analytics.views
import models


def init_cache(app):
    cache = Cache()
    cache.init_app(app)
    return cache


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    init_cache(app)
    app.register_blueprint(bp)

    return app