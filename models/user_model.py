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
