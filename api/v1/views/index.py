#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """return the status of the api"""
    status = {"status": "OK"}
    return jsonify(status)
