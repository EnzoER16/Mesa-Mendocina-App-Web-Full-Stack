from flask import Blueprint, jsonify, request
from config.db import db
from models.plate import Plate
from models.location import Location
from routes.user_routes import token_required

plates_bp = Blueprint('plates', __name__, url_prefix='/api/plates')


@plates_bp.route('/', methods=['GET'])
def get_plates():
    plates = Plate.query.all()

    if not plates:
        return jsonify({'message': 'No hay platos registrados.'}), 200

    return jsonify([plate.to_json() for plate in plates]), 200


@plates_bp.route('/<string:id_plate>', methods=['GET'])
def get_plate(id_plate):
    plate = Plate.query.get(id_plate)
    if not plate:
        return jsonify({"error": "Plato no encontrado"}), 404
    return jsonify(plate.to_json()), 200


@plates_bp.route('/create', methods=['POST'])
@token_required(role="owner")
def create_plate(current_user):
    data = request.get_json()

    if not data or not data.get("name") or not data.get("description") or not data.get("price") or not data.get("id_location"):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    location = Location.query.get(data["id_location"])
    if not location:
        return jsonify({"error": "Local no encontrado"}), 404

    if str(location.id_user) != str(current_user.id_user):
        return jsonify({"error": "No autorizado"}), 403

    new_plate = Plate(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        id_location=data["id_location"])

    db.session.add(new_plate)
    db.session.commit()

    return jsonify(new_plate.to_json()), 201
