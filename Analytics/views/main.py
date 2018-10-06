# -*- coding: utf-8 -*-
from flask import current_app as app, render_template, json, redirect, url_for
from blueprint import bp
from Analytics.application_stat import ApplicationStatsLayout

DEMO_TOKEN = "demo"


@bp.route("/", methods=["GET"])
def index():
    return redirect(url_for(".dashboard", token=DEMO_TOKEN))


@bp.route("/dashboard/<token>", methods=["GET"])
def dashboard(token):
    context = {"token": token}
    return render_template("dashboard.html", **context)


@bp.route("/applications/<token>", methods=["GET"])
def applications(token):
    context = {"token": token}
    return render_template("applications.html", **context)


@bp.route("/candidate-feedback/<token>", methods=["GET"])
def candidate_feedback(token):
    context = {"token": token}
    return render_template("dashboard.html", **context)


@bp.route("/efficiency/<token>", methods=["GET"])
def efficiency(token):
    context = {"token": token}
    return render_template("dashboard.html", **context)


@bp.route("/api/applications", methods=["GET"])
def get_applications_data():
    layout = ApplicationStatsLayout(items=["number_of_view_and_applied"])
    data = layout.get_configurations()
    print data
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@bp.route("/api/dashboard", methods=["GET"])
def get_dashboard_data():
    layout = ApplicationStatsLayout(items=["number_of_view_and_applied"])
    data = layout.get_configurations()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
