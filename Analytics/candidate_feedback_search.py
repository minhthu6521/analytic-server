from flask import json
from flask_babel import gettext
from search import SearchBase, BaseFilter
from copy import deepcopy
from database import db
from models.position_model import Position, REASON_FOR_VACANCY
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
class PositionFilter(Filter):
    id = "position_filter"
    widget = "select2_widget"
    title = gettext(u"Position")

    def set_options(self):
        user = self.context["user"]
        query = db.session.query(Position.internal_name, Position.id).filter_by(company_id=user.company_id)
        return [{
            "value": encode_hash(job_id),
            "label": job_name} for job_name, job_id in query.all()]

    def query_filters(self, context):
        if context["filter"][self.id] and len(context["filter"][self.id]) > 0:
            return [Position.id.in_([decode_hash(pid) for pid in context["filter"][self.id]])]
        return []


@register
class ReasonForVacancyFilter(Filter):
    id = "reason_of_vacancy_filter"
    widget = "checkbox_widget"
    title = gettext(u"Reason for vacancy")

    def set_options(self):
        return REASON_FOR_VACANCY

    def query_filters(self, context):
        if context["filter"][self.id] and len(context["filter"][self.id]) > 0:
            return [Position.reason_for_vacancy.in_(context["filter"][self.id])]
        return []


class CandidateFeedbackSearch(SearchBase):
    FILTERS = Filter
    GENERAL_SEARCH = ["timeframe", "timeframe_custom"]


def get_feedback_search_context(context):
    plan = CandidateFeedbackSearch(context=context)
    return json.dumps(plan.create_search_plan())




