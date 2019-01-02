# -*- coding: utf-8 -*-
import datetime
from flask import current_app as app, render_template, json, redirect, url_for
from blueprint import bp, db
from models import Configuration
import requests
from models.company_model import Company, BusinessUnit
from models.position_model import Position, PositionViewCounter, PositionRights
from models.application_model import Application, ApplicationEvent, ApplicationFeedback, Community, TalentCommunities, Talent
from models.user_model import User


def convert_to_datetime(value, format='%a, %d %b %Y %H:%M:%S %Z'):
    if value:
        return datetime.datetime.strptime(value, format)
    return None


@bp.route("/api/fetch-data", methods=["GET"])
def fetch_data_from_vra():
    fetch_url = app.config["FETCH_URL"]
    config = db.session.query(Configuration).first()
    data = requests.get(fetch_url.format(date=config.last_fetch_date.strftime("%Y-%m-%d") if config else "")).json()
    if data:
        for company in data["company"]:
            new_company = Company(company_token=company["token"],
                                  name=company["name"])
            db.session.add(new_company)
        db.session.flush()
        business_units = data["business_unit"]
        business_units.sort(key=lambda x: x["parent_token"])
        for business_unit in business_units:
            new_bu = BusinessUnit(name=business_unit["name"],
                                  business_unit_token=business_unit["token"],
                                  json_data=business_unit["json_data"])
            company_id = db.session.query(Company.id).filter_by(company_token=business_unit["company_token"]).first()
            if business_unit["parent_token"]:
                parent_id = db.session.query(BusinessUnit.id).filter_by(business_unit_token=business_unit["parent_token"]).first()
                new_bu.parent_id = parent_id[0]
            new_bu.company_id = company_id[0]
            db.session.add(new_bu)
        users = data["user"]
        for user in users:
            new_user = User(user_token=user["token"],
                            first_name=user["first_name"],
                            last_name=user["last_name"],
                            title=user["title"],
                            photoname=user["photoname"],
                            confirmed_at=convert_to_datetime(user["confirmed_at"]),
                            last_login_at=convert_to_datetime(user["last_login_at"]),
                            login_count=user["login_count"],
                            roles=','.join(user["roles"]),
                            password=user["password"],
                            email=user["email"],
                            language=user["language"])
            db.session.add(new_user)
            company_id = db.session.query(Company.id).filter_by(company_token=user["company_token"]).first()
            new_user.company_id = company_id[0]
            db.session.flush()
        positions = data["position"]
        for position in positions:
            new_position = Position(position_token=position["token"],
                                    name=position["name"],
                                    internal_name=position["internal_name"],
                                    language=position["language"],
                                    expiration_date=convert_to_datetime(position["expiration_date"]),
                                    description=position["description"],
                                    template_id=position["template_id"],
                                    link=position["link"],
                                    starting_date=convert_to_datetime(position["starting_date"]),
                                    reason_for_vacancy=position["reason_for_vacancy"],
                                    status=position["status"],
                                    approval_time=convert_to_datetime(position["approval_time"]))
            db.session.add(new_position)
            company_id = db.session.query(Company.id).filter_by(company_token=position["company_token"]).first()
            new_position.company_id = company_id[0]
            user_id = db.session.query(User.id).filter_by(user_token=position["user_token"]).first()
            new_position.user_id = user_id[0]
            business_unit_id = db.session.query(BusinessUnit.id).filter_by(business_unit_token=position["business_unit_token"]).first()
            new_position.business_unit_id = business_unit_id[0]
        db.session.flush()
        position_view_counters = data["position_view_counter"]
        for view in position_view_counters:
            new_view = PositionViewCounter(time=convert_to_datetime(view["time"]))
            db.session.add(new_view)
            position_id = db.session.query(Position.id).filter(position_token=view["job_token"]).first()
            new_view.position_id = position_id
        db.session.flush()
        position_rights = data["position_rights"]
        for position_right in position_rights:
            position_id = db.session.query(Position.id).filter_by(position_token=position_right["job_token"]).first()
            user_id = db.session.query(User.id).filter_by(user_token=position_right["user_token"]).first()
            new_right = PositionRights(role=position_right["role"],
                                       position_id=position_id[0],
                                       user_id=user_id[0],
                                       json_data=position_right["json_data"])
            db.session.add(new_right)
        db.session.flush()
        communities = data["community"]
        for community in communities:
            company_id = db.session.query(Company.id).filter_by(company_token=community["company_token"]).first()
            new_community = Community(company_id=company_id[0],
                                      name=community["name"])
            db.session.add(new_community)
        db.session.flush()
        talents = data["talent"]
        for talent in talents:
            company_id = db.session.query(Company.id).filter_by(company_token=talent["company_token"]).first()

            new_talent = Talent(talent_token=talent["token"],
                                company_id=company_id[0],
                                talent_community=talent["talent_community"],
                                confirmed_talent_community=talent["confirmed_talent_community"],
                                time_confirmed_membership=convert_to_datetime(talent["time_confirmed_membership"]),
                                time_added_to_talent_community=convert_to_datetime(talent["time_added_to_talent_community"]),
                                language=talent["language"],
                                image=talent["image"])
            db.session.add(new_talent)
            db.session.flush()
            for name in talent["talent_communities"]:
                c = db.session.query(Community.id).filter_by(name=name).first()
                db.session.add(TalentCommunities(talent_id=new_talent.id, community_id=c[0]))
        db.session.flush()
        applications = data["application"]
        for application in applications:
            company_id = db.session.query(Company.id).filter_by(company_token=application["company_token"]).first()
            position_id = db.session.query(Position.id).filter_by(position_token=application["position_token"]).first()
            talent_id = db.session.query(Talent.id).filter_by(talent_token=application["talent_token"]).first()
            new_application = Application(application_token=application["token"],
                                          company_id=company_id[0],
                                          position_id=position_id[0],
                                          talent_id=talent_id[0],
                                          status=application["status"],
                                          step=application["step"],
                                          language=application["language"],
                                          application_date=convert_to_datetime(application["application_date"]),
                                          outcome_status=application["outcome_status"],
                                          outcome_email_status=application["outcome_email_status"],
                                          want_feedback=application["want_feedback"],
                                          average_rating=application["average_rating"],
                                          feedback_score=application["feedback_score"],
                                          feedback_rating=application["feedback_rating"],
                                          recommendation_similarity=application["recommendation_similarity"])
            db.session.add(new_application)
        db.session.flush()
        application_events = data["application_event"]
        for event in application_events:
            application_id = db.session.query(Application.id).filter_by(application_token=event["application_token"]).first()
            user_id = db.session.query(User.id).filter_by(user_token=event["user_token"]).first()
            new_event = ApplicationEvent(applicant_id=application_id[0],
                                         application_event_token=event["token"],
                                         user_id=user_id[0],
                                         status=event["status"],
                                         step=event["step"],
                                         time=convert_to_datetime(event["time"]),
                                         note=event["note"],
                                         duration=event["duration"])
            db.session.add(new_event)
        db.session.flush()
        application_feedbacks = data["application_feedback"]
        for feedback in application_feedbacks:
            application_id = db.session.query(Application.id).filter_by(application_token=feedback["application_token"]).first()
            new_feedback = ApplicationFeedback(application_feedback_token=feedback["application_feedback_token"],
                                               application_id=application_id[0],
                                               rating=feedback["rating"],
                                               rating_time=convert_to_datetime(feedback["rating_time"]),
                                               rating_message=feedback["rating_message"])
            db.session.add(new_feedback)
        db.session.flush()
        db.session.commit()
        response = app.response_class(
            response=json.dumps({"notification": "Added successfully!"}),
            status=200,
            mimetype='application/json'
        )
        return response

