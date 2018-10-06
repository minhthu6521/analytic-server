# -*- coding: utf-8 -*-
"""

"""
from copy import deepcopy
import datetime


class BaseStat(object):
    """

    """
    BASE_CONFIGURATION = {
        "id": "",
        "type": "",
        "data": {
            "labels": [],
            "datasets": []
        },
        "options": {
            "title": {
                "display": True,
                "text": ""
            }
        }
    }

    def __init__(self, id=None, context=None, chart_type=None, start=None, end=None):
        if id is not None:
            self.id = id
        self.context = context
        if chart_type is not None:
            self.chart_type = chart_type
        self.start = start
        self.end = end
        self.configuration = deepcopy(self.BASE_CONFIGURATION)

    def get_configuration(self):
        return self.BASE_CONFIGURATION

    def set_title(self, title):
        self.configuration["options"]["title"]["text"] = title

    def get_labels(self):
        pass


class BasePageBlueprint(object):
    def __init__(self, context=None, items=None, start=None, end=None, period=None):
        self.context = context
        self.items = items
        self.start = start
        self.end = end or datetime.datetime.utcnow()
        if period:
            self.end = datetime.datetime.utcnow()
            self.start = datetime.datetime.utcnow() - datetime.timedelta(days=period)

    def get_configurations(self):
        pass