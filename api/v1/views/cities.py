#!/usr/bin/python3
'''
It creates a new view for City objects - handles all default RESTful API actions.
'''

# Importing necessary modules
from flask import abort, jsonify, request
# Importing the State and City models
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


# Route for retrieving all City objects of a specific State
@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    '''
    It Retrieves the list of all City objects of a State.
    '''
    # Gets the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if not state:
        # Returns 404 error if the State object is not found
        abort(404)

    # Gets all City objects associated with
    # the State and convert them to dictionaries
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


# Route for retrieving a specific City object by ID
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''
    It Retrieves a City object.
    '''
    # Gets the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Returns the City object in JSON format
        return jsonify(city.to_dict())
    else:
        # Returns 404 error if the City object is not found
        abort(404)


# Route for deleting a specific City object by ID
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''
    It Deletes a City object.
    '''
    # Gets the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Deletes the City object from the storage and save changes
        storage.delete(city)
        storage.save()
        # Returns an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Returns 404 error if the City object is not found
        abort(404)


# Route for creating a new City object under a specific State
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''
    It Creates a City object.
    '''
    # Gets the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if not state:
        # Returns 404 error if the State object is not found
        abort(404)

    # Checks if the request data is in JSON format
    if not request.get_json():
        # Returns 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Gets the JSON data from the request
    data = request.get_json()
    if 'name' not in data:
        # Returns 400 error if 'name' key is missing in the JSON data
        abort(400, 'Missing name')

    # Assigns the 'state_id' key in the JSON data
    data['state_id'] = state_id
    # Creates a new City object with the JSON data
    city = City(**data)
    # Saves the City object to the storage
    city.save()
    # Returns the newly created City object in JSON format with 201 status code
    return jsonify(city.to_dict()), 201


# Route for updating an existing City object by ID
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
    Updates a City object.
    '''
    # Gets the City object with the given ID from the storage
    city = storage.get(City, city_id)
    if city:
        # Checks if the request data is in JSON format
        if not request.get_json():
            # Returns 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        # Gets the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        # Updates the attributes of the City object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        # Saves the updated City object to the storage
        city.save()
        # Returns the updated City object in JSON format with 200 status code
        return jsonify(city.to_dict()), 200
    else:
        # Returns 404 error if the City object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    404: Not Found.
    '''
    # Returns a JSON response for 404 error
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    Return Bad Request message for illegal requests to API.
    '''
    # Returns a JSON response for 400 error
    return jsonify({'error': 'Bad Request'}), 400

