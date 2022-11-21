#!/usr/bin/python3
"""View for Amenity objects that handles all default
RESTFul API actions
"""


from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, make_response, request, abort
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """Retireves a Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)
    amenity.delete()
    amenity.save()
    return jsonify({})


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """post amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update exsting Aminity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    amenity.save()
    return jsonify(amenity.to_dict())
