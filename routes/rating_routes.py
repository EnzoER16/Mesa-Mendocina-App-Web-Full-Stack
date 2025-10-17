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


@ratings_bp.route('/<string:id_rating>', methods=['GET'])
def get_rating(id_rating):
    rating = Rating.query.get(id_rating)
    if not rating:
        return jsonify({"error": "Valoración no encontrada"}), 404
    return jsonify(rating.to_json()), 200


@ratings_bp.route('/create', methods=['POST'])
@token_required(role="user")
def create_rating(current_user):
    data = request.get_json()

    if not data or not data.get("rate") or not data.get("comment") or not data.get("date") or not data.get("id_location"):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    new_rating = Rating(
        rate=data["rate"],
        comment=data["comment"],
        date=data["date"],
        id_user=current_user.id_user,
        id_location=data["id_location"]
    )

    db.session.add(new_rating)
    db.session.commit()

    return jsonify(new_rating.to_json()), 201

