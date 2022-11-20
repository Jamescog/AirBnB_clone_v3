#!/usr/bin/python3
"""
View for State objects that handels all default RESTFul
API actions
"""


from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_state():
    """handles states requests for GET HTTP method"""
    states = []
    for state in storage.all("State"):
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """retrieve one object of State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_one_state(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    state.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>',
                 methods=['POST'], strict_slashes=False)
def post_one_state(state_id):
    """Create a new state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": 'Missing name'}), 400)

    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update exsting object of state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())
