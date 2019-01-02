# -*- coding: utf-8 -*-
from flask import json
from blueprint import db
from sqlalchemy.orm import relationship
from database import EntityMixin, json_property


class Company(db.Model, EntityMixin):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_token = db.Column(db.String(255))
    name = db.Column(db.String(255))
    positions = db.relationship('Position', lazy='dynamic')
    applicants = db.relationship('Application', lazy='dynamic')
    users = db.relationship('User', lazy='dynamic')

    def __init__(self, company_token, name):
        self.company_token = company_token
        self.name = name


class BusinessUnit(db.Model, EntityMixin):
    __tablename__ = 'business_unit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    business_unit_token = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, db.ForeignKey('business_unit.id', name='business_unit_parent_fk'))
    parent = relationship('BusinessUnit', remote_side=[id])
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', name='business_unit_ibfk_1'), nullable=False)
    company = db.relationship('Company')
    json_data = db.Column(db.Text)

