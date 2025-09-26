from flask import Blueprint, jsonify, request
from config.db import db
from models.location import Location

locations_routes = Blueprint('locations_routes', __name__, url_prefix='/api')

@locations_routes.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()

    if not locations:
        return jsonify({'message': 'No hay locales registrados.'}), 200

    return jsonify([location.to_json() for location in locations]), 200

@locations_routes.route('/locations/get/<string:id_location>', methods=['GET'])
def get_location(id_location):
    location = Location.query.get(id_location)
    if not location:
        return jsonify({"error": "Local no encontrado"}), 404
    return jsonify(location.to_json()), 200

@locations_routes.route('/locations/create', methods=['POST'])
def create_location():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("address") or not data.get("department") or not data.get("schedule") or not data.get("price_range") or not data.get("phone") or not data.get("id_user"):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    new_location = Location(
        name=data["name"],
        address=data["address"],
        department=data["department"],
        schedule=data["schedule"],
        price_range=data["price_range"],
        phone=data["phone"],
        id_user=data["id_user"])

    db.session.add(new_location)
    db.session.commit()

    return jsonify(new_location.to_json()), 201

@locations_routes.route('/location/update/<string:id_location>', methods=['PUT'])
def update_location(id_location):
    location = Location.query.get(id_location)
    if not location:
        return jsonify({"error": "Local no encontrado"}), 404

    data = request.get_json()

    if "name" in data:
        location.name = data["name"]
    if "address" in data:
        location.address = data["address"]
    if "department" in data:
        location.department = data["department"]
    if "schedule" in data:
        location.schedule = data["schedule"]
    if "price_range" in data:
        location.price_range = data["price_range"]
    if "phone" in data:
        location.phone = data["phone"]
    if "id_user" in data:
        location.id_user = data["id_user"]
        
    db.session.commit()
    return jsonify(location.to_json()), 200

@locations_routes.route('/location/delete/<string:id_location>', methods=['DELETE'])
def delete_location(id_location):
    location = Location.query.get(id_location)
    if not location:
        return jsonify({"error": "Local no encontrado"}), 404

    db.session.delete(location)
    db.session.commit()
    return jsonify({"message": "Local eliminado correctamente"}), 200