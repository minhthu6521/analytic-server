# -*- coding: utf-8 -*-

from flask import current_app as app, render_template, json, redirect, url_for
from blueprint import bp, db
from models import Configuration
import requests
from Analytics.actions.import_action import import_company, import_business_unit, import_user, import_position, \
    import_position_view_counter, import_position_rights, import_community, import_talent, import_application, \
    import_applicant_events ,import_application_feedback


@bp.route("/api/fetch-data", methods=["GET"])
def fetch_data_from_vra():
    fetch_url = app.config["FETCH_URL"]
    config = db.session.query(Configuration).first()
    data = requests.get(fetch_url.format(date=config.last_fetch_date.strftime("%Y-%m-%d") if config else "")).json()
    if data:
        import_company(data["company"])
        import_business_unit(data["business_unit"])
        import_user(data["user"])
        import_position(data["position"])
        import_position_view_counter(data["position_view_counter"])
        import_position_rights(data["position_rights"])
        import_community(data["community"])
        import_talent(data["talent"])
        import_application(data["application"])
        import_applicant_events(data["application_event"])
        import_application_feedback(data["application_feedback"])

        db.session.commit()
        response = app.response_class(
            response=json.dumps({"notification": "Added successfully!"}),
            status=200,
            mimetype='application/json'
        )
        return response

