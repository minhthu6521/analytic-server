# -*- coding: utf-8 -*-
from flask import Flask, g, request
from flask_caching import Cache
from flask_babel import Babel
from flask_login import current_user, LoginManager
from database import db
from blueprint import bp
import Analytics.views
import Analytics.actions
import models
from models.user_model import User
from Analytics.utils.hash import hasher


def init_cache(app):
    cache = Cache()
    cache.init_app(app)
    return cache


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    babel = Babel(app)
    init_cache(app)
    app.register_blueprint(bp)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    hasher.init_app(app)

    @babel.localeselector
    def get_locale():
        if current_user.is_authenticated:
            locale = ("en")
        else:
            locale = request.accept_languages.best_match("en")
        return locale

    @app.before_request
    def before_request():
        g.user = current_user
        g.locale = get_locale()

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app