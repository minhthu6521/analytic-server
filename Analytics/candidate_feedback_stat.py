# -*- coding: utf-8 -*-
from flask_babel import gettext
from stat import BasePageBlueprint, BaseStat
from models.application_model import Application, HIRED, REJECTED, \
    OUTCOME_EMAIL_SENT, OUTCOME_EMAIL_BOUNCED, OUTCOME_EMAIL_READ, OUTCOME_EMAIL_NOT_SEND, OUTCOME_DONE_WITHOUT_SEND, \
    ApplicationFeedback
from models.company_model import Company
from models.position_model import Position, PositionViewCounter
from candidate_feedback_search import Filter
from sqlalchemy import func


def register(original_class):
    original_class.register(original_class.id)
    return original_class


class CandidateFeedbackStat(BaseStat):
    stats = {}

    @classmethod
    def register(cls, id):
        if id in CandidateFeedbackStat.stats:
            raise ValueError("Duplicated stat registration")
        CandidateFeedbackStat.stats[id] = cls

    @classmethod
    def stat_for(cls, id):
        return CandidateFeedbackStat.stats.get(id)


@register
class NumberOfReceivedCandidateFeedback(CandidateFeedbackStat):
    id = "number_of_received_candidate_feedback"
    schema = {
        "title": gettext(u"Received Candidate feedback"),
        "items": [
            {
                "display_type": "text",
                "id": "received_candidate_feedback",
                "group_by": "timeframe",
                "criteria": [
                    {
                        "table": ApplicationFeedback,
                        "label": "Feedback from candidates",
                        "filters": [ApplicationFeedback],
                        "op": "total",
                        "time_column": ApplicationFeedback.rating_time,
                        "extra_filters": [lambda x: x.join(Application,
                                                           ApplicationFeedback.application_id == Application.id),
                                          lambda x: x.join(Position,
                                                           Application.position_id == Position.id)],
                    },
                    {
                        "table": ApplicationFeedback,
                        "label": gettext(u"Average rating"),
                        "op": "average",
                        "time_column": ApplicationFeedback.rating_time,
                        "extra_filters": [lambda x: x.join(Application,
                                                           ApplicationFeedback.application_id == Application.id),
                                          lambda x: x.join(Position,
                                                           Application.position_id == Position.id)],
                    }
                ]
            },
            {
                "display_type": "bar_chart",
                "id": "received_and_rating_of_candidate_feedback",
                "group_by": ApplicationFeedback.rating,
                "criteria": [
                    {
                        "table": ApplicationFeedback,
                        "label": "Feedback from candidates",
                        "filters": [ApplicationFeedback.rating, func.count(ApplicationFeedback.id)],
                        "op": "total",
                        "time_column": ApplicationFeedback.rating_time,
                        "extra_filters": [lambda x: x.join(Position,
                                                           Application.position_id == Position.id)],
                        "display": {
                            "backgroundColor": "rgba(235,192,235,0.2)",
                            "borderColor": "rgba(235,192,235,1)",
                        }
                    }
                ]
            }
        ]
    }


class CandidateFeedbackStatsLayout(BasePageBlueprint):
    items = CandidateFeedbackStat.stats.keys()
    item_class = CandidateFeedbackStat

    def extra_filters(self):
        filters = []
        for key in self.context["filter"].keys():
            filter = Filter.criterion_for(key)(context={"user": self.context["user"]}).query_filters(self.context)
            if len(filter) > 0:
                filters = filters + filter
        filters = filters + [Application.company_id == self.context["user"].company_id]
        return filters
