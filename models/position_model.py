# -*- coding: utf-8 -*-
from blueprint import db
from database import EntityMixin


class Position(db.Model, EntityMixin):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    language = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', name='job_ibfk_1'))
    company = db.relationship('Company')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="job_user_fk"))
    user = db.relationship('User')
    duedate = db.Column(db.DateTime)
    description = db.Column(db.Text)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id', name='job_ibfk_2'))
    link = db.Column(db.String(2047))
    startdate = db.Column(db.DateTime)
    employment_type = db.Column(db.String(255))

    status = db.Column(db.Integer, default=6)
    reviewers = db.relationship('JobApproval')
    approval_time = db.Column(db.DateTime)

    active_applications = db.relationship("Application",
                                          primaryjoin='and_(Application.job_id==Job.id,'
                                                      'Application.is_removed == False)',
                                          viewonly=True)


class PositionViewCounter(db.Model, EntityMixin):
    __tablename__ = 'ad_view_counters'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)