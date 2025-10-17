from flask import Blueprint, jsonify, request
from config.db import db
from models.plate import Plate
from models.location import Location
from routes.user_routes import token_required

plates_bp = Blueprint('plates', _name_, url_prefix='/api/plates')

@plates_bp.route('/', methods=['GET'])
def get_plates():
    plates = Plate.query.all()

    if not plates:
        return jsonify({'message': 'No hay platos registrados.'}), 200

    return jsonify([plate.to_json() for plate in plates]), 200
