# -*- coding: utf-8 -*-
from blueprint import db
from database import EntityMixin


class User(db.Model, EntityMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), default="")
    last_name = db.Column(db.String(255), default="")
    title = db.Column(db.String(255), default="")


    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company')
    photoname = db.Column(db.String(255))

    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role',
                            secondary="roles_users",
                            backref=db.backref('users', lazy='dynamic'))

