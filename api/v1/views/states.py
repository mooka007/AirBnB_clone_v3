#!/usr/bin/python3
"""
Creates a new view for State objects - handles all default RESTful API actions.
"""

# Importing necessary modules
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage

# Route for retrieving all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects.
    """
    # Gets all State objects from the storage
    states = storage.all(State).values()
    # Converts objects to dictionaries and jsonify the list
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)

# Route for retrieving a specific State object by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object.
    """
    # Gets the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if state:
        # Returns the State object in JSON format
        return jsonify(state.to_dict())
    else:
        # Returns 404 error if the State object is not found
        abort(404)

# Route for deleting a specific State object by ID
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object.
    """
    # Gets the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if state:
        # Deletes the State object from the storage and save changes
        storage.delete(state)
        storage.save()
        # Returns an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Returns 404 error if the State object is not found
        abort(404)

# Route for creating a new State object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object.
    """
    if not request.get_json():
        # Returns 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Gets the JSON data from the request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # Returns 400 error if 'name' key is missing in the JSON data
        abort(400, 'Missing name')

    # Creates a new State object with the JSON data
    state = State(**kwargs)
    # Saves the State object to the storage
    state.save()
    # Returns the newly created State object in JSON format with 201 status code
    return jsonify(state.to_dict()), 201

# Routes for updating an existing State object by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.
    """
    # Gets the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            # Returns 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Gets the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Updates the attributes of the State object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        # It saves the updated State object to the storage
        state.save()
        # It returns the updated State object in JSON format with 200 status code
        return jsonify(state.to_dict()), 200
    else:
        # It returns 404 error if the State object is not found
        abort(404)

# Error Handlers:

@app_views.errorhandler(404)
def not_found(error):
    """
    Raises a 404 error.
    """
    # It returns a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def bad_request(error):
    """
    Returns a Bad Request message for illegal requests to the API.
    """
    # It returns a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400

