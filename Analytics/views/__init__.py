from flask import url_for

import main
import external
from blueprint import bp


@bp.context_processor
def context_all():
    context = {}
    context["nav_list"] = [
        {
            "label": "Dashboard",
            "id": "dashboard",
            "url": url_for(".dashboard"),
            "icon": "",
            "hidden": False
        },
        {
            "label": "Applications",
            "id": "dashboard",
            "url": url_for(".applications"),
            "icon": "",
            "hidden": False
        },
        {
            "label": "Candidate feedback",
            "id": "dashboard",
            "url": url_for(".candidate_feedback"),
            "icon": "",
            "hidden": True
        },
        {
            "label": "Efficiency",
            "id": "dashboard",
            "url": url_for(".efficiency"),
            "icon": "",
            "hidden": True
        },
    ]
    return context