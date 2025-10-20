from flask import Blueprint, jsonify, request
from config.db import db
from models.location import Location
from routes.user_routes import token_required

locations_bp = Blueprint('locations', __name__, url_prefix='/api/locations')

@locations_bp.route('/', methods=['GET'])
def get_locations():
    locations = Location.query.all()

    if not locations:
        return jsonify({'message': 'No hay locales registrados.'}), 200

    return jsonify([location.to_json() for location in locations]), 200

@locations_bp.route('/<string:id_location>', methods=['GET'])
def get_location(id_location):
    location = Location.query.get(id_location)
    if not location:
        return jsonify({"error": "Local no encontrado"}), 404
    return jsonify(location.to_json()), 200

@locations_bp.route('/create', methods=['POST'])
@token_required(role="owner")
def create_location(current_user):
    data = request.get_json()

    if not data or not data.get("name") or not data.get("address") or not data.get("department") or not data.get("schedule") or not data.get("price_range") or not data.get("phone"):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    new_location = Location(
        name=data["name"],
        address=data["address"],
        department=data["department"],
        schedule=data["schedule"],
        price_range=data["price_range"],
        phone=data["phone"],
        id_user=current_user.id_user)

    db.session.add(new_location)
    db.session.commit()

    return jsonify(new_location.to_json()), 201

@locations_bp.route('/edit/<string:id_location>', methods=['PUT'])
@token_required(role="owner")
def edit_location(current_user, id_location):
    location = Location.query.get(id_location)
    if not location:
        return jsonify({"error": "Local no encontrado"}), 404

    if location.id_user != current_user.id_user:
        return jsonify({"error": "No autorizado"}), 403

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
        
    db.session.commit()
    return jsonify(location.to_json()), 200

@locations_bp.route('/delete/<string:id_location>', methods=['DELETE'])
@token_required(role="owner")
def delete_location(current_user, id_location):
    location = Location.query.get(id_location)
    if not location:
        return jsonify({"error": "Local no encontrado"}), 404
    
    if location.id_user != current_user.id_user:
        return jsonify({"error": "No autorizado"}), 403

    db.session.delete(location)
    db.session.commit()
    return jsonify({"message": "Local eliminado correctamente"}), 200