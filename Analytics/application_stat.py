# -*- coding: utf-8 -*-
from flask_babel import gettext
from stat import BasePageBlueprint, BaseStat
from models.application_model import Application, HIRED, REJECTED, \
    OUTCOME_EMAIL_SENT, OUTCOME_EMAIL_BOUNCED, OUTCOME_EMAIL_READ
from models.company_model import Company
from models.position_model import Position, PositionViewCounter
from recruitment_process_search import Filter


def register(original_class):
    original_class.register(original_class.id)
    return original_class


class ApplicationStat(BaseStat):
    stats = {}

    @classmethod
    def register(cls, id):
        if id in ApplicationStat.stats:
            raise ValueError("Duplicated stat registration")
        ApplicationStat.stats[id] = cls

    @classmethod
    def stat_for(cls, id):
        return ApplicationStat.stats.get(id)


@register
class NumberOfViewAndApplied(ApplicationStat):
    id = "number_of_view_and_applied"
    schema = {
        "title": gettext(u"Views and applied"),
        "items": [
            {
                "display_type": "line_chart",
                "id": "view_and_applied_line",
                "group_by": "timeframe",
                "criteria": [
                    {
                        "table": PositionViewCounter,
                        "group_column": PositionViewCounter.time,
                        "label": "View",
                        "op": "count",
                        "time_column": PositionViewCounter.time,
                        "extra_filters": [lambda x: x.join(Position, Position.id == PositionViewCounter.position_id)],
                        "display": {
                            "backgroundColor": "rgba(235,192,235,0.2)",
                            "borderColor": "rgba(235,192,235,1)",
                        }
                    },
                    {
                        "table": Application,
                        "group_column": Application.application_date,
                        "op": "count",
                        "label": "Applied",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position)],
                        "display": {
                            "backgroundColor": "rgba(246,120,120,0.2)",
                            "borderColor": "rgba(246,120,120,1)",
                        }
                    }
                ]
            },
            {
                "display_type": "text",
                "id": "view_and_applied_percentage",
                "group_by": "timeframe",
                "criteria": [
                    {
                        "op": "percentage",
                        "divisor": "View",
                        "dividend": "Applied",
                        "label": "Percentage"
                    },
                    {
                        "table": PositionViewCounter,
                        "label": "View",
                        "op": "total",
                        "time_column": PositionViewCounter.time,
                        "extra_filters": [lambda x: x.join(Position, Position.id == PositionViewCounter.position_id)],
                    },
                    {
                        "table": Application,
                        "op": "total",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position)],
                        "label": "Applied"
                    }
                ]
            }
        ]
    }


@register
class RejectAndHired(ApplicationStat):
    id = "hired_and_reject"
    schema = {
        "title": gettext(u"Hired and reject"),
        "items": [
            {
                "display_type": "line_chart",
                "id": "hired_and_reject_line",
                "group_by": "timeframe",
                "criteria": [
                    {
                        "table": Application,
                        "group_column": Application.application_date,
                        "label": "Rejected",
                        "op": "count",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.filter(Application.outcome_status == REJECTED)],
                        "display": {
                            "backgroundColor": "rgba(235,192,235,0.2)",
                            "borderColor": "rgba(235,192,235,1)",
                        }
                    },
                    {
                        "table": Application,
                        "group_column": Application.application_date,
                        "op": "count",
                        "label": "Hired",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.filter(Application.outcome_status == HIRED)],
                        "display": {
                            "backgroundColor": "rgba(246,120,120,0.2)",
                            "borderColor": "rgba(246,120,120,1)",
                        }
                    }
                ]
            },
            {
                "display_type": "text",
                "id": "hired_and_reject_total",
                "group_by": "timeframe",
                "criteria": [
                    {
                        "table": Application,
                        "op": "total",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position),
                                          lambda x: x.filter(Application.outcome_status == REJECTED)],
                        "label": "Rejected"
                    },
                    {
                        "table": Application,
                        "op": "total",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position),
                                          lambda x: x.filter(Application.outcome_status == HIRED)],
                        "label": "Hired"
                    },
                    {
                        "table": Application,
                        "op": "total",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position),
                                          lambda x: x.filter(Application.outcome_status == REJECTED,
                                                             Application.outcome_email_status \
                                                             .in_([OUTCOME_EMAIL_SENT, OUTCOME_EMAIL_BOUNCED,
                                                                   OUTCOME_EMAIL_READ]))],
                        "label": "Feedback sent"
                    }
                ]
            }
        ]
    }


class ApplicationStatsLayout(BasePageBlueprint):
    items = ApplicationStat.stats.keys()
    item_class = ApplicationStat

    def extra_filters(self):
        filters = []
        for key in self.context["filter"].keys():
            filter = Filter.criterion_for(key)(context={"user": self.context["user"]}).query_filters(self.context)
            if len(filter) > 0:
                filters = filters + filter
        filters = filters + [Position.company_id == self.context["user"].company_id]
        return filters
