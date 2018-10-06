from flask import Blueprint
from database import db

bp = Blueprint('analytics', __name__, template_folder='Analytics/templates')