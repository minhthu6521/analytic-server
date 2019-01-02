from Analytics.statistics import BaseCategory, BaseResultPlan
from models.application_model import Application
from database import db


def register(original_class):
    original_class.register(original_class.id)
    return original_class


class Category(BaseCategory):
    categories = {}

    @classmethod
    def register(cls, id):
        if id in Category.categories:
            raise ValueError("Duplicated criterion registration")
        Category.categories[id] = cls

    @classmethod
    def category_for(cls, id):
        return Category.categories.get(id)


@register
class TotalViewAndApplied(Category):
    id = "total_view_and_applied"
    widget = "basic_text"
    operation = ["sum"]
    title = "Total views and applied"
    tables = [Application]

    def get_data(self):
        view = db.session.query(Application).group_by



@register
class PercentageViewAndApplied(Category):
    id = "percentage_view_and_applied"
    widget = "line_graph"
    operation = ["percentage", "count"]
    title = "View and Applied"


@register
class HiredRejectAndWithdrawnApplications(Category):
    id = "hired_and_rejected"
    widget = "line_graph"
    operation = ["count"]
    title = "Applications with outcome"




