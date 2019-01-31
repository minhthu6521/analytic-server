# -*- coding: utf-8 -*-
from flask_babel import gettext
from stat import BasePageBlueprint, BaseStat
from models.application_model import Application, HIRED, REJECTED, WITHDRAWN, \
    OUTCOME_EMAIL_SENT, OUTCOME_EMAIL_BOUNCED, OUTCOME_EMAIL_READ, ApplicationEvent, \
    OUTCOME_EMAIL_NOT_SEND
from models.company_model import Company
from models.position_model import Position, PositionViewCounter
from recruitment_process_search import Filter
from sqlalchemy import and_, Date, cast
from blueprint import db


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
                        "filters": [PositionViewCounter.time],
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
                        "filters": [Application.application_date],
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
                        "type": "View",
                        "label": "View",
                        "filters": [PositionViewCounter],
                        "op": "total",
                        "time_column": PositionViewCounter.time,
                        "extra_filters": [lambda x: x.join(Position, Position.id == PositionViewCounter.position_id)],
                    },
                    {
                        "table": Application,
                        "filters": [Application],
                        "op": "total",
                        "type": "Applied",
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
                "display_type": "pie_chart",
                "id": "hired_and_reject_pie",
                "group_by": "timeframe",
                "criteria": [
                    {
                        "table": Application,
                        "label": "Rejected",
                        "filters": [Application],
                        "op": "total",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position),
                                          lambda x: x.filter(Application.outcome_status == REJECTED)],
                        "display": {
                            "backgroundColor": "rgba(235,192,235,1)"
                        }
                    },
                    {
                        "table": Application,
                        "label": "Withdrawn",
                        "filters": [Application],
                        "op": "total",
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position),
                                          lambda x: x.filter(Application.outcome_status == WITHDRAWN)],
                        "display": {
                            "backgroundColor": "rgba(213,422,235,1)"
                        }
                    },
                    {
                        "table": Application,
                        "op": "total",
                        "label": "Hired",
                        "filters": [Application],
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position),
                                          lambda x: x.filter(Application.outcome_status == HIRED)],
                        "display": {
                            "backgroundColor": "rgba(246,120,120,1)"
                        }
                    },
                    {
                        "table": Application,
                        "op": "total",
                        "filters": [Application],
                        "time_column": Application.application_date,
                        "extra_filters": [lambda x: x.join(Position),
                                          lambda x: x.filter(Application.outcome_status == None)],
                        "display": {
                            "backgroundColor": "rgba(66, 182, 244, 1)"
                        },
                        "label": "Processing"
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
                        "filters": [Application],
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


@register
class ProcessingTime(ApplicationStat):
    id = "processing_time"

    def __init__(self, id=None, context=None):
        super(ApplicationStat, self).__init__(id, context)
        self.schema = {
            "title": gettext(u"Processing time"),
            "items": [
                {
                    "display_type": "text",
                    "id": "average_processing_time_text",
                    "criteria": [
                        {
                            "table": Application,
                            "op": "custom",
                            "filters": [Application],
                            "time_column": Application.application_date,
                            "extra_filters": [],
                            "label": "Average processing time",
                            "custom_conf": self.average_time
                        }
                    ]
                }
            ]
        }

    def process_time_data(self, start, end):
        applications = db.session.query(Application.application_date, Application.id) \
                         .filter(Application.company_id == self.context["user"].company_id,
                                 Application.outcome_email_status.notin_([None, OUTCOME_EMAIL_NOT_SEND]),
                                 and_(cast(Application.application_date, Date) < self.end,
                                      cast(Application.application_date, Date) > self.start),
                                 Application.outcome_status.isnot(None)).all()
        outcome_events = db.session.query(ApplicationEvent.time, ApplicationEvent.application_id).join(Application)\
                           .filter(Application.company_id == self.context["user"].company_id,
                                   ApplicationEvent.status_update == True,
                                   ApplicationEvent.outcome_status.isnot(None),
                                   and_(cast(Application.application_date, Date) < self.end,
                                        cast(Application.application_date, Date) > self.start),
                                   Application.outcome_status.isnot(None)).all()
        process_time = []
        for application in applications:
            end_process_time = [event[0] for event in outcome_events if event[1] == application[1]][0]
            process_time.append((application[0], end_process_time))
        return process_time

    def average_time(self, start, end):
        process_time = self.process_time_data(start, end)
        average = []
        for time in process_time:
            average.append((time[1] -time[0]).days)
        return sum(average) // len(average)


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
