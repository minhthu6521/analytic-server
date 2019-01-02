# -*- coding: utf-8 -*-
"""

"""
from copy import deepcopy
import datetime
from dateutil.relativedelta import relativedelta
from blueprint import db
from sqlalchemy import and_


class BaseStat(object):
    """

    """
    start = None
    end = None
    schema = None
    BASE_SCHEMA = {
        "title": u"",
        "items": [
        ]
    }

    def __init__(self, id=None, context=None):
        if id is not None:
            self.id = id
        self.context = context
        if self.schema is None:
            self.schema = deepcopy(self.BASE_SCHEMA)
        self._timeframe()

    def _timeframe(self):
        if self.context["filter"].get("timeframe") != "custom":
            now = datetime.datetime.utcnow().date()
            self.start = now - datetime.timedelta(days=self.context["filter"].get("timeframe"))
            self.end = now
        else:
            self.start = self.context["filter"]["start"]
            self.end = self.context["filter"]["end"]

    def _group_by(self, item):
        groups = []
        if item["group_by"] == "timeframe":
            period = int(self.context["filter"].get("timeframe")) \
                if self.context["filter"].get("timeframe") != "custom" else (self.end - self.start).days()
            if period < 300:
                divider = period / 10
                date = self.start
                while date < self.end:
                    groups.append({"point": date,
                                   "label": date.strftime("%Y-%m-%d")})
                    date = date + datetime.timedelta(days=divider)
            elif period < 12 * 30:
                date = self.start
                while date < self.end:
                    groups.append({"point": date.replace(day=1),
                                   "label": date.strftime("%B")})
                    date = date + relativedelta(months=+1)
            else:
                date = self.start.replace(day=1)
                divider = (period / 30) / 10
                while date < self.end:
                    groups.append({"point": date,
                                   "label": date.strftime("%B")})
                    date = date + relativedelta(months=+divider)

        return groups

    def _convert_data_to_line_chart_data(self, criteria, group_by):
        dataset = []
        if group_by == "timeframe" and criteria["op"] == "count":
            query = db.session.query(criteria["group_column"]) \
                .filter(and_(criteria["time_column"] < self.end,
                             criteria["time_column"] > self.start))
            raw_data = query.all()
            groups = self._group_by(criteria)
            for index, point in enumerate(groups):
                if index < len(groups) - 2:
                    count = len([d for (d,) in raw_data if d > point["point"] and d <= groups[index + 1]["point"]])
                    dataset.append(count)
            return dataset

    def get_line_chart_conf(self, item):
        conf = {
            "labels": [p["label"] for p in self._group_by(item)],
            "dataset": []
        }
        for criteria in item["criteria"]:
            criteria_conf = {
                "data": self._convert_data_to_line_chart_data(criteria, item.get("group_by")),
                "label": criteria.get("label")
            }
            criteria_conf.update(criteria.get("display"))
            conf["dataset"].append(criteria_conf)
        return conf

    def get_configurations(self):
        configurations = {
            "id": self.id,
            "title": self.schema.get("title"),
            "items": [
            ]
        }
        for item in self.schema.get("items"):
            item_conf = {
                "id": item["id"],
                "display_type": item["display_type"],
                "data": {}
            }
            if item["display_type"] == "line_chart":
                item_conf["data"] = self.get_line_chart_conf(item)
            configurations["items"].append(item_conf)
        return configurations


class BasePageBlueprint(object):
    id = None

    def __init__(self, context=None, items=None):
        self.context = context
        if items is not None:
            self.items = items


