from flask import url_for

import main
from blueprint import bp


@bp.context_processor
def context_all():
    context = {}
    context["nav_list"] = [
        {
            "label": "Dashboard",
            "id": "dashboard",
            "url": url_for(".dashboard", token=main.DEMO_TOKEN),
            "icon": "",
            "hidden": False
        },
        {
            "label": "Applications",
            "id": "dashboard",
            "url": url_for(".applications", token=main.DEMO_TOKEN),
            "icon": "",
            "hidden": False
        },
        {
            "label": "Candidate feedback",
            "id": "dashboard",
            "url": url_for(".candidate_feedback", token=main.DEMO_TOKEN),
            "icon": "",
            "hidden": True
        },
        {
            "label": "Efficiency",
            "id": "dashboard",
            "url": url_for(".efficiency", token=main.DEMO_TOKEN),
            "icon": "",
            "hidden": True
        },
    ]
    return context