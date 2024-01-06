#!/usr/bin/python3
"""Host of our Flask app"""

from flask import Flask, Blueprint, render_template, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tearDown(self):
    """Closes storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(self):
    """ handles 404 error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", "5000"), threaded=True)
