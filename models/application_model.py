# -*- coding: utf-8 -*-
from blueprint import db
from database import EntityMixin


class Application(db.Model, EntityMixin):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    job = db.relationship('Job')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company')
    status = db.Column(db.Integer, default=0)
    step = db.Column(db.String(255))
    is_sent = db.Column(db.Boolean, default=False)
    f_lang = db.Column(db.Integer)
    application_date = db.Column(db.DateTime)

    outcome_status = db.Column(db.Integer)

    want_feedback = db.Column(db.Boolean, default=True, server_default='1')

    # These are cached for faster sorting, etc
    average_rating = db.Column(db.Float, default=None)
    feedback_score = db.Column(db.Float, default=None)
    feedback_rating = db.Column(db.Float, default=None)
    recommendation_similarity = db.Column(db.Float, default=None)
