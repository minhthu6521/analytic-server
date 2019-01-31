# -*- coding: utf-8 -*-
from blueprint import db
from database import EntityMixin

PENDING = "pending"
CONFIRMED = "confirmed"
REJECTED_SLOT = "rejected"

class InterviewSlot(db.Model):

    __tablename__ = 'interview_slot'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    begins = db.Column(db.DateTime, nullable=False)
    ends = db.Column(db.DateTime, nullable=False)
    for_applicant_status = db.Column(db.Integer)
    step = db.Column(db.String(255))
    note = db.Column(db.Text)
    visibility = db.Column(db.String(64), default='visible', server_default='visible')


class OfferedSlot(db.Model):

    __tablename__ = 'offered_slot'
    slot_id = db.Column(db.Integer, db.ForeignKey('interview_slot.id', name='offered_slot_ibfk_2'), primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('application.id', name='offered_slot_ibfk_1'), primary_key=True)
    confirmation = db.Column(db.String(64), default=PENDING)
    step = db.Column(db.String(255))

    slot = db.relationship("InterviewSlot", backref=db.backref('offered_to_applicants', cascade="all, delete-orphan"))
    applicant = db.relationship("Application", backref=db.backref('offered_slots', cascade="all, delete-orphan"))