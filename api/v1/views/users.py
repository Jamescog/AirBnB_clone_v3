#!/usr/bin/python3
"""
View for User object that handles
all default RESTFul API actions
"""


from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = []
    for user in storage.all("User").values():
        users.append(user.to_ditct())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', strict_slashes=False)
def get_user(user_id):
    """Retrieves a User Object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    user.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_one_user():
    """Create a new User"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({"error": 'email'}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)

    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(state_id):
    """Update exsting object of user"""
    user = storage.get("User", state_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict())
