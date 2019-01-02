import company_model
import user_model
import position_model
import application_model
from blueprint import db


class Configuration(db.Model):
    __tablename__ = "configuration"

    id = db.Column(db.Integer, primary_key=True)
    last_fetch_date = db.Column(db.DateTime())

