# -*- coding: utf-8 -*-
from flask_babel import gettext
from stat import BasePageBlueprint, BaseStat
from models.application_model import Application
from models.company_model import Company
from models.position_model import Position, PositionViewCounter


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
    """
    {
        "id": "number_of_view_and_applied",
        "display_type": "line",
        "criteria": [
            {
                "table": PositionViewCounter,
                "op": count,
                "time_column": time,
                "extra_filter: {},
                "group_by": "timeframe"
            },
            {
                "table": Application,
                "op": count,
                "time_column": application_date,
                "extra_filter": {},
                "group_by": "timeframe"
            }
        ]
    }
    """
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
                            "extra_filter": None,
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
                            "extra_filter": None,
                            "display": {
                                "backgroundColor": "rgba(246,120,120,0.2)",
                                "borderColor": "rgba(246,120,120,1)",
                            }
                        }
                    ]
                }
            ]
        }


class ApplicationStatsLayout(BasePageBlueprint):
    items = ApplicationStat.stats.keys()

    def get_configurations(self):
        configurations = []
        for item in self.items:
            stat = ApplicationStat.stat_for(item)(context=self.context)
            configurations.append(stat.get_configurations())
        return configurations
