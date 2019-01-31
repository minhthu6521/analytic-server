# -*- coding: utf-8 -*-
from blueprint import db
from database import EntityMixin


ADMIN = 'admin'
DEMO = 'demo'
READER = 'reader'
HIRING_MANAGER = 'hiring_manager'
PILOT = 'pilot'
RECRUITER = 'recruiter'


class User(db.Model, EntityMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), default="")
    last_name = db.Column(db.String(255), default="")
    title = db.Column(db.String(255), default="")
    user_token = db.Column(db.String(255))

    company_id = db.Column(db.Integer, db.ForeignKey('company.id', name='company_userfk_1'))
    company = db.relationship('Company')
    photoname = db.Column(db.String(255))
    language = db.Column(db.Integer)

    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer)
    roles = db.Column(db.Text)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))


class Task(db.Model, EntityMixin):
    __tablename__ = 'user_task'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id])
    due_time = db.Column(db.DateTime)
    assigner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigner = db.relationship('User', foreign_keys=[assigner_id])
    is_done = db.Column(db.Boolean, default=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id', name='application_task_1'))
    application = db.relationship('Application')