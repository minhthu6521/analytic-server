# -*- coding: utf-8 -*-
import datetime
from blueprint import bp, db

from models.company_model import Company, BusinessUnit
from models.position_model import Position, PositionViewCounter, PositionRights
from models.application_model import Application, ApplicationEvent, ApplicationFeedback, Community, TalentCommunities, Talent
from models.user_model import User


def convert_to_datetime(value, format='%a, %d %b %Y %H:%M:%S %Z'):
    if value:
        return datetime.datetime.strptime(value, format)
    return None


def import_company(data):
    for company in data["company"]:
        old_company = db.session.query(Company).filter_by(company_token=company["token"]).first()
        if not old_company:
            new_company = Company(company_token=company["token"],
                                  name=company["name"])
            db.session.add(new_company)
        else:
            old_company.name = company["name"]
    db.session.flush()


def import_business_unit(data):
    data.sort(key=lambda x: x["parent_token"])
    for business_unit in data:
        old_bu = db.session.query(BusinessUnit).filter_by(business_unit_token=business_unit["token"]).first()
        if not old_bu:
            new_bu = BusinessUnit(name=business_unit["name"],
                                  business_unit_token=business_unit["token"],
                                  json_data=business_unit["json_data"])
            company_id = db.session.query(Company.id).filter_by(company_token=business_unit["company_token"]).first()
            if business_unit["parent_token"]:
                parent_id = db.session.query(BusinessUnit.id).filter_by(
                    business_unit_token=business_unit["parent_token"]).first()
                new_bu.parent_id = parent_id[0]
            new_bu.company_id = company_id[0]
            db.session.add(new_bu)
        else:
            old_bu.name = business_unit["name"]
            old_bu.json_data = business_unit["json_data"]


def import_user(data):
    for user in data:
        old_user = db.session.query(User).filter_by(user_token=user["token"]).first()
        if not old_user:
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
        else:
            old_user.first_name = user["first_name"]
            old_user.last_name = user["last_name"]
            old_user.title = user["title"]
            old_user.photoname = user["photoname"]
            old_user.confirmed_at = convert_to_datetime(user["confirmed_at"])
            old_user.last_login_at = convert_to_datetime(user["last_login_at"])
            old_user.login_count = user["login_count"]
            old_user.roles = ','.join(user["roles"])
            old_user.password = user["password"]
            old_user.email = user["email"]
            old_user.language = user["language"]


def import_position(data):
    for position in data:
        old_position = db.session.query(Position).filter_by(position_token=position["token"]).first()
        if not old_position:
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
            business_unit_id = db.session.query(BusinessUnit.id).filter_by(
                business_unit_token=position["business_unit_token"]).first()
            new_position.business_unit_id = business_unit_id[0]
            db.session.flush()
        else:
            old_position.name = position["name"]
            old_position.internal_name = position["internal_name"]
            old_position.language = position["language"]
            old_position.expiration_date = convert_to_datetime(position["expiration_date"])
            old_position.description = position["description"]
            old_position.template_id = position["template_id"]
            old_position.link = position["link"]
            old_position.starting_date = convert_to_datetime(position["starting_date"])
            old_position.reason_for_vacancy = position["reason_for_vacancy"]
            old_position.status = position["status"]
            old_position.approval_time = convert_to_datetime(position["approval_time"])


def import_position_view_counter(data):
    for view in data:
        position_id = db.session.query(Position.id).filter_by(position_token=view["job_token"]).first()
        new_view = PositionViewCounter(time=convert_to_datetime(view["time"]),
                                       position_id=int(position_id[0]))
        db.session.add(new_view)
        db.session.flush()


# NEED TO CHECK BELOW
def import_position_rights(data):
    for position_right in data:
        position_id = db.session.query(Position.id).filter_by(position_token=position_right["job_token"]).first()
        user_id = db.session.query(User.id).filter_by(user_token=position_right["user_token"]).first()
        new_right = PositionRights(role=position_right["role"],
                                   position_id=position_id[0],
                                   user_id=user_id[0],
                                   json_data=position_right["json_data"])
        db.session.add(new_right)
    db.session.flush()


def import_community(data):
    for community in data:
        company_id = db.session.query(Company.id).filter_by(company_token=community["company_token"]).first()
        old_community = db.session.query(Community).filter_by(company_id=company_id[0],
                                  name=community["name"]).first()
        if not old_community:
            new_community = Community(company_id=company_id[0],
                                      name=community["name"])
            db.session.add(new_community)
        db.session.flush()


def import_talent(data):
    for talent in data:
        old_talent = Talent.query.filter_by(talent_token=talent["token"]).first()
        if not old_talent:
            company_id = db.session.query(Company.id).filter_by(company_token=talent["company_token"]).first()

            new_talent = Talent(talent_token=talent["token"],
                                company_id=company_id[0],
                                talent_community=talent["talent_community"],
                                confirmed_talent_community=talent["confirmed_talent_community"],
                                time_confirmed_membership=convert_to_datetime(talent["time_confirmed_membership"]),
                                time_added_to_talent_community=convert_to_datetime(
                                    talent["time_added_to_talent_community"]),
                                language=talent["language"])
            db.session.add(new_talent)
            db.session.flush()
            for name in talent["talent_communities"]:
                c = db.session.query(Community.id).filter_by(name=name).first()
                db.session.add(TalentCommunities(talent_id=new_talent.id, community_id=c[0]))
        else:
            old_talent.talent_community = talent["talent_community"]
            old_talent.confirmed_talent_community = talent["confirmed_talent_community"]
            old_talent.time_confirmed_membership = convert_to_datetime(talent["time_confirmed_membership"])
            old_talent.time_added_to_talent_community = convert_to_datetime(talent["time_added_to_talent_community"])
            old_talent.language = talent["language"]
        db.session.flush()


def import_application(data):
    for application in data:
        old_application = Application.query.filter_by(application_token=application["token"]).first()
        if not old_application:
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
        else:
            old_application.status = application["status"]
            old_application.step = application["step"]
            old_application.language = application["language"]
            old_application.application_date = convert_to_datetime(application["application_date"])
            old_application.outcome_status = application["outcome_status"]
            old_application.outcome_email_status = application["outcome_email_status"]
            old_application.want_feedback = application["want_feedback"]
            old_application.average_rating = application["average_rating"]
            old_application.feedback_score = application["feedback_score"]
            old_application.feedback_rating = application["feedback_rating"]
            old_application.recommendation_similarity = application["recommendation_similarity"]
        db.session.flush()


def import_applicant_events(data):
    for event in data:
        application_id = db.session.query(Application.id).filter_by(
            application_token=event["application_token"]).first()
        if event["user_token"]:
            user_id = db.session.query(User.id).filter_by(user_token=event["user_token"]).first()
        new_event = ApplicationEvent(application_id=application_id[0],
                                     application_event_token=event["token"],
                                     user_id=user_id[0] or None,
                                     status=event["status"],
                                     step=event["step"],
                                     time=convert_to_datetime(event["time"]),
                                     status_update=event["status_update"],
                                     outcome_status=event["outcome_status"],
                                     note=event["note"],
                                     duration=event["duration"])
        db.session.add(new_event)
    db.session.flush()


def import_application_feedback(data):
    for feedback in data:
        application_id = db.session.query(Application.id).filter_by(
            application_token=feedback["application_token"]).first()
        new_feedback = ApplicationFeedback(application_feedback_token=feedback["application_feedback_token"],
                                           application_id=int(application_id[0]),
                                           rating=feedback["rating"],
                                           rating_time=convert_to_datetime(feedback["rating_time"]),
                                           rating_message=feedback["rating_message"])
        db.session.add(new_feedback)
    db.session.flush()