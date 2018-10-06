# -*- coding: utf-8 -*-
from stat import BasePageBlueprint, BaseStat


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
    chart_type = "line"

    def set_configuration(self):
        self.configuration["type"] = self.chart_type
        self.configuration["data"]["labels"] = ["January", "February", "March", "April", "May", "June", "July"]
        self.set_title("Applications/View ratio")
        self.configuration["id"] = self.id
        self.configuration["data"]["datasets"] = [
            {"backgroundColor": "rgba(235,192,235,0.2)",
             "borderColor": "rgba(235,192,235,1)",
             "data": [65, 59, 80, 81, 56, 55, 40],
             "label": "View"
             },
            {"backgroundColor": "rgba(246,120,120,0.2)",
             "borderColor": "rgba(246,120,120,1)",
             "data": [28, 48, 40, 19, 86, 27, 90],
             "label": "Applied"
             }
        ]


class ApplicationStatsLayout(BasePageBlueprint):
    def get_configurations(self):
        configurations = []
        for item in self.items:
            stat = ApplicationStat.stat_for(item)()
            stat.set_configuration()
            configurations.append(stat.configuration)
        return configurations
