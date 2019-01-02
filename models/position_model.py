# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from blueprint import db
from database import EntityMixin, json_property
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship, backref


DRAFT, ACTIVE, EXPIRED, ARCHIVED, DELETED, INACTIVE, PENDING, WAITING_FOR_APPROVAL, APPROVED = range(1, 10)


CLASSIC_TEMPLATE = "classic"
MODERN_TEMPLATE = "modern"
PLAYFUL_TEMPLATE = "playful"
ELEGANT_TEMPLATE = "elegant"
SIMPLE_TEMPLATE = "simple"

TEMPLATES = {
    CLASSIC_TEMPLATE: lazy_gettext(u"Classic template"),
    MODERN_TEMPLATE: lazy_gettext(u"Modern template"),
    PLAYFUL_TEMPLATE: lazy_gettext(u"Playful template"),
    ELEGANT_TEMPLATE: lazy_gettext(u"Elegant template"),
    SIMPLE_TEMPLATE: lazy_gettext(u"Simple template")
}

OPEN_APPLICATION = u"For open applications"
REASON_FOR_VACANCY = [(u"", lazy_gettext(u"Unspecified")),
                      (u"New position", lazy_gettext(u"New position")),
                      (OPEN_APPLICATION, lazy_gettext(u"For open applications")),
                      (u"Maternity leave", lazy_gettext(u"Maternity leave")),
                      (u"Parental leave", lazy_gettext(u"Parental leave")),
                      (u"Annual leave", lazy_gettext(u"Annual leave")),
                      (u"Project", lazy_gettext(u"Project")),
                      (u"Resignation", lazy_gettext(u"Resignation")),
                      (u"Retirement", lazy_gettext(u"Retirement")),
                      (u"Replacement", lazy_gettext(u"Replacement")),
                      (u"Secondment", lazy_gettext(u"Secondment")),
                      (u"Other leave", lazy_gettext(u"Other leave"))]


class Position(db.Model, EntityMixin):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    position_token = db.Column(db.String(255))
    name = db.Column(db.String(255))
    internal_name = db.Column(db.String(255))
    language = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', name='position_ibfk_1'))
    company = db.relationship('Company')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="position_user_fk"))
    user = db.relationship('User')
    expiration_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    template_id = db.Column(db.String(255))
    link = db.Column(db.String(2047))
    starting_date = db.Column(db.DateTime)
    employment_type = db.Column(db.String(255))
    reason_for_vacancy = db.Column(db.String(255))
    business_unit_id = db.Column(db.Integer, db.ForeignKey('business_unit.id', name="job_business_unit_fk"))
    business_unit = db.relationship('BusinessUnit', backref=backref('jobs', lazy='dynamic'))

    status = db.Column(db.Integer, default=INACTIVE)
    approval_time = db.Column(db.DateTime)

    active_applications = db.relationship("Application",
                                          primaryjoin='and_(Application.position_id==Position.id)',
                                          viewonly=True)


class PositionRights(db.Model, EntityMixin):
    __tablename__ = 'position_rights'
    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id', name='position_right_position_fk'))
    position = relationship("Position", backref=backref("rights", cascade="all, delete-orphan", viewonly=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='position_right_user_fk1'))
    user = relationship("User", backref=backref("jobs_has_rights_to", cascade="all, delete-orphan", viewonly=True))
    role = db.Column(db.String(64))
    json_data, data = json_property('json_data', db.Column(MEDIUMTEXT), default={})


class PositionViewCounter(db.Model, EntityMixin):
    __tablename__ = 'ad_view_counters'
    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)