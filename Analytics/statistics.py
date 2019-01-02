import datetime


class BaseCategory(object):
    def __init__(self, id=None, widget=None, context=None, title=None, configurations=None, operation=None):
        if id is not None:
            assert getattr(self, 'id', id) == id
            self.id = id
        self.context = context or {}
        self.configurations = configurations
        if widget is not None:
            self.widget = widget
        if title:
            self.title = title
        if operation:
            self.operation = operation

    def get_data(self):
        pass

    def prepare_data(self):
        pass



class BaseResultPlan():
    CATEGORIES = None
    EMPTY_PLAN = {
        "items": []
    }

    def __init__(self, plan=None, values=None, context=None):
        self.context = context or {}
        self.plan = plan or self.EMPTY_PLAN
        self.values = self.initial_values() if values is None else values

    def initial_values(self):
        return {}

    def create_plan(self):
        pass


def get_display_range(starttime, endtime, interval=10):
    timeframe = (endtime - starttime).days
    if timeframe < interval:
        result = [starttime + datetime.timedelta(days=i) for i in range(0, timeframe + 1)]
    else:
        difference = int(timeframe / interval)
        result = [starttime + datetime.timedelta(days=i) for i in range(0, timeframe + 1, difference)]
    if not endtime in result:
        result = result[:-1]
        result.append(endtime)
    return result