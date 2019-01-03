import datetime
from flask_babel import gettext
from copy import deepcopy
from sqlalchemy import and_, not_, or_


class BaseFilter(object):
    def __init__(self, id=None, widget=None, context=None, enums=None, configurations=None, title=None):
        if id is not None:
            assert getattr(self, 'id', id) == id
            self.id = id
        self.context = context or {}
        self.enums = enums or []
        self.configurations = configurations
        if widget is not None:
            self.widget = widget
        if title:
            self.title = title

    def items(self):
        return self.enums

    def set_options(self):
        pass

    def set_configuration(self):
        pass

    def query_filters(self, context):
        return []


class SearchBase(object):
    FILTERS = None
    OPERATIONS_MAP = {
        'or': or_,
        'and': and_,
        'not': not_,
    }

    EMPTY_PLAN = {
        'op': 'and',
        'general': {
            'header': "Filter for general stats",
            'items': []
        },
        'specific': {
            'header': "Specific positions",
            'items': []
        },
        'default': {}
    }
    GENERAL_SEARCH = []
    SPECIFIC_SEARCH = []

    def __init__(self, plan=None, values=None, context=None):
        self.context = context or {}
        self.plan = plan or self.EMPTY_PLAN
        self.values = self.initial_values() if values is None else values

    def initial_values(self):
        return {}

    def create_search_plan(self):
        plan = deepcopy(self.plan)
        for filter_id in self.FILTERS.filters:
            filter = self.FILTERS.filters[filter_id](context=self.context)
            _obj =  {
                        "id": filter.id,
                        "type": filter.widget,
                        "context": {
                            "title": filter.title or "",
                            "options": filter.set_options(),
                            "configuration": filter.set_configuration()
                        }
                    }
            if filter_id in self.GENERAL_SEARCH:
                plan['general']["items"].append(_obj)
            else:
                plan['specific']["items"].append(_obj)
            if filter.default:
                plan['default'].update({filter_id: filter.default})
        self.plan = plan
        return self.plan
