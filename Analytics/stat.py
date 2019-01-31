# -*- coding: utf-8 -*-
"""

"""
from copy import deepcopy
import datetime
from dateutil.relativedelta import relativedelta
from blueprint import db
from sqlalchemy import and_, Date, cast
from flask_babel import gettext


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
            self.start = now - datetime.timedelta(days=int(self.context["filter"].get("timeframe")))
            self.end = now
        else:
            self.start = self.context["filter"]["start"]
            self.end = self.context["filter"]["end"]

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
            item_obj = StatItem.item_for(item["display_type"])(self.context, self.start, self.end, item)
            item_conf["data"] = item_obj.get_conf()
            configurations["items"].append(item_conf)
        return configurations


def register(original_class):
    original_class.register(original_class.id)
    return original_class


class StatItem(object):
    id=None
    start = None
    end = None
    items = {}
    default = None

    @classmethod
    def register(cls, id):
        if id in StatItem.items:
            raise ValueError("Duplicated item registration")
        StatItem.items[id] = cls

    @classmethod
    def item_for(cls, id):
        return StatItem.items.get(id)

    def __init__(self, context=None, start=None, end=None, item=None):
        if id is not None:
            self.id = id
        self.context = context
        self.start = start
        self.end = end
        self.item = item

    def _group_by(self):
        groups = []
        if self.item.get("group_by") == "timeframe":
            period = int(self.context["filter"].get("timeframe")) \
                if self.context["filter"].get("timeframe") != "custom" else (self.end - self.start).days()
            if period < 60:
                date = self.start
                while date < self.end:
                    groups.append({"point": date,
                                   "label": date.strftime("%d-%m-%Y")})
                    date = date + datetime.timedelta(days=1)
            elif period < 12 * 30:
                date = self.start
                while date < self.end:
                    groups.append({"point": date.replace(day=1),
                                   "label": date.strftime("%B-%y")})
                    date = date + relativedelta(months=1)
            else:
                date = self.start.replace(day=1)
                divider = (period / 30) / 10
                while date < self.end:
                    groups.append({"point": date,
                                   "label": date.strftime("%B-%y")})
                    date = date + relativedelta(months=divider)
        else:
            # The group_by column should be the first filter result
            query = db.session.query(self.item["group_by"]).distinct()
            groups = [{"label": d[0],
                       "point": d[0]} for d in query]
        return groups

    def _filters(self, criteria):
        filters = [and_(cast(criteria["time_column"], Date) < self.end,
                       cast(criteria["time_column"], Date) > self.start)]
        if self.context["extra_filters"]:
            for efilter in self.context["extra_filters"]:
                filters.append(efilter)
        return filters

    def _get_data(self, criteria):
        if criteria.get("filters"):
            query = db.session.query(*criteria["filters"])
            for filter in self._filters(criteria):
                query = query.filter(filter)
            if criteria.get("extra_filters"):
                for cfilter in criteria["extra_filters"]:
                    query = cfilter(query)
            if "count" in criteria["op"]:
                if criteria.get("group_by"):
                    query = query.group_by(criteria["group_by"])
                data = query.all()
            elif "total" in criteria["op"]:
                data = query.count()
            else:
                data = query.all()
            return data

    def convert_data(self, criteria):
        pass

    def get_conf(self):
        pass


@register
class LineChartItem(StatItem):
    id = "line_chart"

    def convert_data(self, criteria):
        datasets = []
        if self.item["group_by"] == "timeframe":
            raw_data = self._get_data(criteria)
            groups = self._group_by()
            for index, point in enumerate(groups):
                if index < len(groups) - 1:
                    count = len([d.date() for (d,) in raw_data if d.date() > point["point"] and d.date() <= groups[index + 1]["point"]])
                    datasets.append(count)
            return datasets

    def get_conf(self):
        conf = {
            "labels": [p["label"] for p in self._group_by()[1:]],
            "datasets": []
        }
        for criteria in self.item["criteria"]:
            criteria_conf = {
                "data": self.convert_data(criteria),
                "label": criteria.get("label")
            }
            criteria_conf.update(criteria.get("display"))
            conf["datasets"].append(criteria_conf)
        return conf


@register
class BarChartItem(StatItem):
    id = "bar_chart"

    def convert_data(self, criteria):
        datasets = []
        if self.item.get("group_by") == "timeframe":
            raw_data = self._get_data(criteria)
            groups = self._group_by()
            for index, point in enumerate(groups):
                if index < len(groups) - 1:
                    count = len([d.date() for (d,) in raw_data if d.date() > point["point"] and d.date() <= groups[index + 1]["point"]])
                    datasets.append(count)
        else:
            raw_data = self._get_data(criteria)
            groups = self._group_by()
            for index, point in enumerate(groups):
                result = [data[1] for data in raw_data if data[0] == point["point"]][0]
                datasets.append(result)
        return datasets

    def get_conf(self):
        groups = self._group_by()
        groups = groups[1:] if self.item.get("group_by") == "timeframe" else groups
        conf = {
            "labels": [p["label"] for p in groups],
            "datasets": []
        }
        for criteria in self.item["criteria"]:
            criteria_conf = {
                "data": self.convert_data(criteria),
                "label": criteria.get("label")
            }
            criteria_conf.update(criteria.get("display"))
            conf["datasets"].append(criteria_conf)
        return conf


@register
class PieChartItem(StatItem):
    id = "pie_chart"

    def convert_data(self, criteria):
        datasets = []
        raw_data = self._get_data(criteria)
        if "total" in criteria["op"]:
            datasets.append(raw_data)
        return datasets

    def get_conf(self):
        conf = {
            "labels": [],
            "datasets": []
        }
        dataset_obj = {
            "fill": True,
            "backgroundColor": [],
            "data": [],
        }
        for criteria in self.item["criteria"]:
            dataset_obj["backgroundColor"].append(criteria.get("display").get("backgroundColor"))
            dataset_obj["data"].append(self.convert_data(criteria))
            conf["labels"].append(criteria.get("label"))
        conf["datasets"].append(dataset_obj)
        return conf


@register
class TextDisplayItem(StatItem):
    id = "text"

    def convert_data(self, criteria):
        datasets = []
        raw_data = self._get_data(criteria)
        if "total" in criteria["op"]:
            datasets.append(raw_data)
        if "percentage" in criteria["op"]:
            divisor = [c for c in self.item["criteria"] if criteria["divisor"] == c.get("type")]
            dividend = [c for c in self.item["criteria"] if criteria["dividend"] == c.get("type")]
            if self._get_data(divisor[0]) == 0:
                datasets.append(gettext(u"Cannot calculate"))
            else:
                percentage = round(self._get_data(dividend[0]) / (self._get_data(divisor[0]) * 1.0), 4) * 100
                datasets.append(str(percentage) + "%")
        if "average" in criteria["op"]:
            if raw_data and len(raw_data) > 0:
                average = round(sum(raw_data) / float(len(raw_data)), 2)
                datasets.append(average)
        if "custom" in criteria["op"]:
            datasets.append(criteria["custom_conf"](self.start, self.end))
        return datasets

    def get_conf(self):
        conf = {
            "datasets": []
        }
        for criteria in self.item["criteria"]:
            criteria_conf = {
                "data": self.convert_data(criteria),
                "label": criteria.get("label")
            }
            conf["datasets"].append(criteria_conf)
        return conf


class BasePageBlueprint(object):
    id = None
    item_class = None

    def __init__(self, context=None, items=None):
        self.context = context
        if items is not None:
            self.items = items

    def extra_filters(self):
        pass

    def get_configurations(self):
        configurations = []
        for item in self.items:
            context = self.context
            context["extra_filters"] = self.extra_filters()
            stat = self.item_class.stat_for(item)(context=context)
            configurations.append(stat.get_configurations())
        return configurations

