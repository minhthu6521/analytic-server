# -*- coding: utf-8 -*-
from flask import current_app as app, render_template
from blueprint import bp


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")