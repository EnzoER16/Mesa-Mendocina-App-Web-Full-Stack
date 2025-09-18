from flask import Blueprint, request, jsonify, render_template
from config.db import db
from models.user import User

# Definición del Blueprint para las rutas de usuario
users_routes = Blueprint('users_routes', __name__, url_prefix='/api')

# Ruta para obtener todos los usuarios
@users_routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users]), 200

# Ruta para obtener un usuario por su ID
@users_routes.route('/users/get/<string:id_user>', methods=['GET'])
def get_user(id_user):
    user = User.query.get(id_user)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.to_json()), 200

# Ruta para crear un nuevo usuario
@users_routes.route('/users/create', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validar que se proporcionen todos los campos necesarios
    if not data or not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Verificar si ya existe el email
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    # Crear un nuevo usuario
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"])

    # Guardar el nuevo usuario en la base de datos
    db.session.add(new_user)
    db.session.commit()

    # Devolver la respuesta con el usuario creado
    return jsonify(new_user.to_json()), 201

# Ruta para actualizar un usuario existente
@users_routes.route('/users/update/<string:id_user>', methods=['PUT'])
def update_user(id_user):
    user = User.query.get(id_user)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        # Verificar que el nuevo email no esté ya en uso
        if User.query.filter_by(email=data["email"]).first() and user.email != data["email"]:
            return jsonify({"error": "El email ya está en uso"}), 400
        user.email = data["email"]
    if "password" in data:
        user.__init__(user.name, user.email, data["password"])  # Re-hashear password

    db.session.commit()
    return jsonify(user.to_json()), 200

# Ruta para eliminar un usuario
@users_routes.route('/users/delete/<string:id_user>', methods=['DELETE'])
def delete_user(id_user):
    user = User.query.get(id_user)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado correctamente"}), 200