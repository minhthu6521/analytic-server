# -*- coding: utf-8 -*-
from flask_babel import gettext
from stat import BasePageBlueprint, BaseStat
from models.application_model import Application, HIRED, REJECTED, \
    OUTCOME_EMAIL_SENT, OUTCOME_EMAIL_BOUNCED, OUTCOME_EMAIL_READ, OUTCOME_EMAIL_NOT_SEND, OUTCOME_DONE_WITHOUT_SEND, \
    ApplicationEvent
from models.user_model import Task
from models.company_model import Company
from models.position_model import Position, PositionViewCounter
from models.interview_slot_model import InterviewSlot, OfferedSlot, CONFIRMED
from efficiency_search import Filter
from utils.hash import decode_hash


def register(original_class):
    original_class.register(original_class.id)
    return original_class


class EfficiencyStat(BaseStat):
    stats = {}

    @classmethod
    def register(cls, id):
        if id in EfficiencyStat.stats:
            raise ValueError("Duplicated stat registration")
        EfficiencyStat.stats[id] = cls

    @classmethod
    def stat_for(cls, id):
        return EfficiencyStat.stats.get(id)


@register
class NumberOfOpenPositions(EfficiencyStat):
    id = "number_of_open_positions"

    def __init__(self, id=None, context=None):
        super(EfficiencyStat, self).__init__(id, context)
        self.schema = {
            "title": gettext(u"Number of open positions"),
            "items": [
                {
                    "display_type": "text",
                    "id": "number_of_positions_opened",
                    "criteria": [
                        {
                            "table": Position,
                            "filters": [Position],
                            "op": "total",
                            "time_column": Position.time_created,
                            "extra_filters": [lambda x: x.filter(Position.user_id == decode_hash(self.context["filter"]["user_filter"]))],
                            "label": gettext(u"Positions opened")
                        }
                    ]
                }
            ]
        }


@register
class NumberOfProcessedApplications(EfficiencyStat):
    id = "number_of_processed_applications"

    def __init__(self, id=None, context=None):
        super(EfficiencyStat, self).__init__(id, context)
        self.schema = {
            "title": gettext(u"Number of processed applications"),
            "items": [
                {
                    "display_type": "text",
                    "id": "number_of_processed_applications",
                    "criteria": [
                        {
                            "table": ApplicationEvent,
                            "filters": [ApplicationEvent],
                            "op": "total",
                            "time_column": ApplicationEvent.time,
                            "extra_filters": [
                                lambda x: x.distinct(ApplicationEvent.application_id),
                                lambda x: x.filter(ApplicationEvent.user_id == decode_hash(self.context["filter"]["user_filter"]))],
                            "label": gettext(u"Number of processed applications")
                        }
                    ]
                }
            ]
        }

@register
class NumberOfTasksGiven(EfficiencyStat):
    id = "number_of_tasks_given"

    def __init__(self, id=None, context=None):
        super(EfficiencyStat, self).__init__(id, context)
        self.schema = {
            "title": gettext(u"Tasks"),
            "items": [
                {
                    "display_type": "text",
                    "id": "number_of_tasks_given",
                    "criteria": [
                        {
                            "table": Task,
                            "filters": [Task],
                            "op": "total",
                            "time_column": Task.time_created,
                            "extra_filters": [
                                lambda x: x.filter(Task.user_id == decode_hash(self.context["filter"]["user_filter"]),
                                                   Task.assigner_id.isnot(None))],
                            "label": gettext(u"Number of tasks given")
                        }
                    ]
                },
                {
                    "display_type": "text",
                    "id": "number_of_completed_tasks",
                    "criteria": [
                        {
                            "table": Task,
                            "filters": [Task],
                            "op": "total",
                            "time_column": Task.time_created,
                            "extra_filters": [
                                lambda x: x.filter(Task.user_id == decode_hash(self.context["filter"]["user_filter"]),
                                                   Task.assigner_id.isnot(None),
                                                   Task.is_done == True)],
                            "label": gettext(u"Number of completed given tasks")
                        }
                    ]
                },
                {
                    "display_type": "text",
                    "id": "number_of_tasks_to_others",
                    "criteria": [
                        {
                            "table": Task,
                            "filters": [Task],
                            "op": "total",
                            "time_column": Task.time_created,
                            "extra_filters": [
                                lambda x: x.filter(Task.assigner_id == decode_hash(self.context["filter"]["user_filter"]))],
                            "label": gettext(u"Number of tasks gave to others")
                        }
                    ]
                }
            ]
        }


@register
class NumberOfInterviews(EfficiencyStat):
    id = "number_of_interviews"

    def __init__(self, id=None, context=None):
        super(EfficiencyStat, self).__init__(id, context)
        self.schema = {
            "title": gettext(u"Interviews"),
            "items": [
                {
                    "display_type": "text",
                    "id": "number_of_tasks_given",
                    "criteria": [
                        {
                            "table": OfferedSlot,
                            "filters": [OfferedSlot],
                            "op": "total",
                            "time_column": InterviewSlot.begins,
                            "extra_filters": [
                                lambda x: x.join(InterviewSlot),
                                lambda x: x.filter(InterviewSlot.user_id == decode_hash(self.context["filter"]["user_filter"]),
                                                   OfferedSlot.confirmation == CONFIRMED)],
                            "label": gettext(u"Number of interviews given")
                        }
                    ]
                }
            ]
        }


class EfficiencyStatsLayout(BasePageBlueprint):
    items = EfficiencyStat.stats.keys()
    item_class = EfficiencyStat

    def extra_filters(self):
        filters = []
        for key in self.context["filter"].keys():
            filter = Filter.criterion_for(key)(context={"user": self.context["user"]}).query_filters(self.context)
            if len(filter) > 0:
                filters = filters + filter
        filters = filters + [Position.company_id == self.context["user"].company_id]
        return filters
