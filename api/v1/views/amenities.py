#!/usr/bin/python3
"""View for Amenity objects that handles all default
RESTFul API actions
"""


from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, make_response, request, abort,
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = []
    for amenity in storage.all("Amenity"):
        amenities.append(amenity)
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """Retireves a Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity)


@app_views.route('/amenities/<sting:amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)
    amenity.delete()
    amenity.save()
    return jsonify({})


#@app_views.route('/amenities', methods=['POST'], strict_slashes=False)

