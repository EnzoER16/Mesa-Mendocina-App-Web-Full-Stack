from flask import Blueprint, jsonify, request
from config.db import db
from models.rating import Rating
from routes.user_routes import token_required

ratings_bp = Blueprint('ratings', __name__, url_prefix='/api/ratings')

@ratings_bp.route('/', methods=['GET'])
def get_ratings():
    ratings = Rating.query.all()

    if not ratings:
        return jsonify({'message': 'No hay valoraciones registradas.'}), 200

    return jsonify([rating.to_json() for rating in ratings]), 200
