# -*- coding: utf-8 -*-
from blueprint import db
from database import EntityMixin


class Company(db.Model, EntityMixin):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    jobs = db.relationship('Job', lazy='dynamic')
    applicants = db.relationship('Application', lazy='dynamic')
    users = db.relationship('User', lazy='dynamic')
    access_token = db.Column(db.String(255), nullable=False)

