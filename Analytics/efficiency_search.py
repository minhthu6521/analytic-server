from flask import json
from flask_babel import gettext
from search import SearchBase, BaseFilter
from copy import deepcopy
from database import db
from models.position_model import Position, REASON_FOR_VACANCY
from models.user_model import User
from Analytics.utils.hash import encode_hash, decode_hash


def register(original_class):
    original_class.register(original_class.id)
    return original_class


class Filter(BaseFilter):
    filters = {}
    default = None

    @classmethod
    def register(cls, id):
        if id in Filter.filters:
            raise ValueError("Duplicated criterion registration")
        Filter.filters[id] = cls

    @classmethod
    def criterion_for(cls, id):
        return Filter.filters.get(id)

    def query_filters(self, context):
        return []


@register
class DateRangeSelection(Filter):
    id = "timeframe"
    widget = "dropdown_widget"
    title = gettext(u"Select time")
    default = 30

    def set_options(self):
        return [(30, gettext(u"Past 30 days")),
                (180, gettext(u"Past six months")),
                (365, gettext(u"Past year")),
                ("custom", gettext(u"Custom timeframe"))]


@register
class CustomDateTimeFilter(Filter):
    id = "timeframe_custom"
    widget = "datetime_widget"
    title = gettext(u"Custom time frame")

    def set_configuration(self):
        return {
            "mindate": None
        }


@register
class UserFilter(Filter):
    id = "user_filter"
    widget = "dropdown_widget"
    title = gettext(u"Select user")

    def set_options(self):
        user = self.context["user"]
        query = db.session.query(User.last_name, User.first_name, User.id).filter_by(company_id=user.company_id)
        options = [(encode_hash(user_id), lastname + " " + firstname) for lastname, firstname, user_id in query.all()]
        self.default = options[0][0]
        return options

    def query_filters(self, context):
        if context["filter"][self.id] and len(context["filter"][self.id]) > 0:
            return [User.id.in_([decode_hash(context["filter"][self.id])])]
        return []


class EfficiencySearch(SearchBase):
    FILTERS = Filter
    GENERAL_SEARCH = ["timeframe", "timeframe_custom"]


def get_efficiency_search_context(context):
    plan = EfficiencySearch(context=context)
    return json.dumps(plan.create_search_plan())




