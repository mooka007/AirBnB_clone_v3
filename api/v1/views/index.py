#!/usr/bin/python3
"""Creates a route that returns a JSON"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def return_jsonify():
    """Returns JSON status=OK"""
    return jsonify({"status": "OK"})
