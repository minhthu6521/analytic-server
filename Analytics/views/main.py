# -*- coding: utf-8 -*-
from flask import current_app as app, render_template, json
from blueprint import bp


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/<type>", methods=["GET"])
def dashboard(type):
    return render_template("index.html")


@bp.route("/api/dashboard", methods=["GET"])
def get_dashboard_data():
    data = [
        {
            'id': "testchart",
            'type': 'bar',
            'data': {
                'labels': ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
                'datasets': [{
                    'label': '# of Votes',
                    'data': [12, 19, 3, 5, 2, 3],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    'borderColor': [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    'borderWidth': 1
                }]
            },
            'options': {
                'scales': {
                    'yAxes': [{
                        'ticks': {
                            'beginAtZero': True
                        }
                    }]
                },
                'responsive': True
            }
        },
        {
            'id': 'scatterchart',
            'type': 'scatter',
            'data': {
                'datasets': [{
                    'label': 'Scatter Dataset',
                    'data': [{
                        'x': -10,
                        'y': 0
                    }, {
                        'x': 0,
                        'y': 10
                    }, {
                        'x': 10,
                        'y': 5
                    }]
                }]
            },
            'options': {
                'scales': {
                    'xAxes': [{
                        'type': 'linear',
                        'position': 'bottom'
                    }]
                }
            }
        }
    ]
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@bp.route("/api/feedback", methods=["GET"])
def get_feedback_data():
    data = [
        {
            'id': "feedback",
            'type': 'bar',
            'data': {
                'labels': ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
                'datasets': [{
                    'label': '# of Votes',
                    'data': [12, 19, 3, 5, 2, 3],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    'borderColor': [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    'borderWidth': 1
                }]
            },
            'options': {
                'scales': {
                    'yAxes': [{
                        'ticks': {
                            'beginAtZero': True
                        }
                    }]
                },
                'responsive': True
            }
        },
        {
            'id': 'feedback1',
            'type': 'scatter',
            'data': {
                'datasets': [{
                    'label': 'Scatter Dataset',
                    'data': [{
                        'x': -10,
                        'y': 0
                    }, {
                        'x': 0,
                        'y': 10
                    }, {
                        'x': 10,
                        'y': 5
                    }]
                }]
            },
            'options': {
                'scales': {
                    'xAxes': [{
                        'type': 'linear',
                        'position': 'bottom'
                    }]
                }
            }
        }
    ]
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response