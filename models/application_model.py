# -*- coding: utf-8 -*-
from flask import json
import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects import mysql
from flask_babel import lazy_gettext

from blueprint import db
from database import EntityMixin

(NEW_APPLICANT, APPLICATION_REVIEW, PHONE_INTERVIEW, FACE_TO_FACE, OFFER, REJECTED, TALENT_COMMUNITY,
 VIDEO_INTERVIEW, CUSTOM_STATUS, ASSIGNMENT, WITHDRAWN, HIRED, UNHIRED, UNREJECTED, UNWITHDRAWN) = range(15)

APPLICANT_STATUSES = {
    NEW_APPLICANT: lazy_gettext("New"),
    APPLICATION_REVIEW: lazy_gettext("Application review"),
    PHONE_INTERVIEW: lazy_gettext("Phone interview"),
    FACE_TO_FACE: lazy_gettext("Face to face interview"),
    OFFER: lazy_gettext("Offer"),
}

OUTCOME_STATUSES = {
    HIRED: lazy_gettext("Hired"),
    REJECTED: lazy_gettext("Rejected"),
    WITHDRAWN: lazy_gettext("Withdrawn"),
}

OUTCOME_EMAIL_SENT = "sent"
OUTCOME_EMAIL_NOT_SEND = "not_send"
OUTCOME_DONE_WITHOUT_SEND = "done_without_send"
OUTCOME_EMAIL_READ = "read"
OUTCOME_EMAIL_BOUNCED = "bounced"


class Community(db.Model, EntityMixin):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer,
                           db.ForeignKey('company.id', name='community_ibfk_1', ondelete="CASCADE"))
    name = db.Column(db.String(255))

    def __init__(self, name, company_id):
        self.name = name
        self.company_id = company_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class TalentCommunities(db.Model, EntityMixin):
    __tablename__ = 'talent_communities'
    talent_id = db.Column(db.Integer, db.ForeignKey('talent.id', name="talent_communities_talent_fk", ondelete="CASCADE"),
                          primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id', name="talent_communities_community_fk", ondelete="CASCADE"),
                             primary_key=True)

    talent = db.relationship("Talent")
    community = db.relationship("Community")

    def __init__(self, talent_id, community_id):
        self.talent_id = talent_id
        self.community_id = community_id


class Talent(db.Model, EntityMixin):
    __tablename__ = 'talent'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', name='company_talent_fk'))
    talent_token = db.Column(db.String(255), nullable=False)
    company = db.relationship('Company')

    talent_community = db.Column(db.Boolean, default=False, server_default='0')
    confirmed_talent_community = db.Column(db.Boolean, default=False, server_default='0')
    applications = db.relationship('Application',
                                   cascade="all, delete-orphan")
    talent_communities = db.relationship('TalentCommunities', cascade="all, delete-orphan")
    communities = association_proxy('talent_communities', 'community')
    time_confirmed_membership = db.Column(db.DateTime)
    time_added_to_talent_community = db.Column(db.DateTime, default=None)
    language = db.Column(db.Integer)


class Application(db.Model, EntityMixin):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    application_token = db.Column(db.String(255))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id', name='application_position_fk'))
    position = db.relationship('Position')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', name='application_company_fk'))
    company = db.relationship('Company')
    talent_id = db.Column(db.Integer, db.ForeignKey('talent.id', name='application_talent_fk'))
    talent = db.relationship('Talent')
    status = db.Column(db.Integer, default=0)
    step = db.Column(db.String(255))
    language = db.Column(db.Integer)
    application_date = db.Column(db.DateTime)

    outcome_status = db.Column(db.Integer)
    outcome_email_status = db.Column(db.String(255))

    want_feedback = db.Column(db.Boolean, default=True, server_default='1')

    json_ratings = db.Column(mysql.MEDIUMTEXT(), default=json.dumps({}))

    average_rating = db.Column(db.Float, default=None)
    feedback_score = db.Column(db.Float, default=None)
    feedback_rating = db.Column(db.Float, default=None)
    recommendation_similarity = db.Column(db.Float, default=None)
    events = db.relationship("ApplicationEvent", cascade="all, delete-orphan")

    @property
    def ratings(self):
        if self.json_ratings:
            return json.loads(self.json_ratings)
        return {}


class ApplicationEvent(db.Model, EntityMixin):
    __tablename__ = 'application_event'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    application = db.relationship('Application')
    application_event_token = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    status = db.Column(db.Integer)
    status_update = db.Column(db.Boolean, default=0, server_default=db.text('0'))
    outcome_status = db.Column(db.Integer, nullable=True)
    step = db.Column(db.String(255))
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    note = db.Column(db.String(255))
    duration = db.Column(db.Integer, nullable=True)


class ApplicationFeedback(db.Model, EntityMixin):
    __tablename__ = 'application_feedback'
    id = db.Column(db.Integer, primary_key=True)
    application_feedback_token = db.Column(db.String(255))
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'),
                             nullable=False)
    application = db.relationship('Application')
    rating = db.Column(db.Integer)
    rating_time = db.Column(db.DateTime())
    rating_message = db.Column(db.Text)
