# -*- coding: utf-8 -*-
from flask import current_app as app, render_template, json, redirect, url_for, request
from flask_login import current_user
from blueprint import bp
from Analytics.application_stat import ApplicationStatsLayout
from Analytics.efficiency_stat import EfficiencyStatsLayout
from Analytics.recruitment_process_search import get_application_search_context
from Analytics.candidate_feedback_search import get_feedback_search_context
from Analytics.efficiency_search import get_efficiency_search_context
from Analytics.candidate_feedback_stat import CandidateFeedbackStatsLayout
from models.user_model import User

DEMO_TOKEN = "demo"


@bp.route("/", methods=["GET"])
def index():
    return redirect(url_for(".dashboard", token=DEMO_TOKEN))


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    token = None
    context = {"token": token}
    return render_template("dashboard.html", **context)


@bp.route("/applications", methods=["GET"])
def applications():
    context = {"search_plan": get_application_search_context({"user": current_user})}
    return render_template("applications.html", **context)


@bp.route("/candidate-feedback", methods=["GET"])
def candidate_feedback():
    context = {"search_plan": get_feedback_search_context({"user": current_user})}
    return render_template("candidate_feedback.html", **context)


@bp.route("/efficiency", methods=["GET"])
def efficiency():
    context = {"search_plan": get_efficiency_search_context({"user": current_user})}
    return render_template("efficiency.html", **context)


@bp.route("/api/applications", methods=["GET"])
def get_applications_data():
    filter = json.loads(request.args["data"])
    layout = ApplicationStatsLayout(context={"filter": filter,
                                             "user": current_user})
    data = layout.get_configurations()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@bp.route("/api/efficiency", methods=["GET"])
def get_users_data():
    filter = json.loads(request.args["data"])
    layout = EfficiencyStatsLayout(context={"filter": filter,
                                            "user": current_user})
    data = layout.get_configurations()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@bp.route("/api/candidate-feedback", methods=["GET"])
def get_candidate_feedback_data():
    filter = json.loads(request.args["data"])
    layout = CandidateFeedbackStatsLayout(context={"filter": filter,
                                                   "user": current_user})
    data = layout.get_configurations()
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
