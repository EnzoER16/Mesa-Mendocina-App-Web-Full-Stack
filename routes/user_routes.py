import jwt
from flask import current_app as app
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Blueprint, request, jsonify, render_template
from config.db import db
from models.user import User

# Definición del Blueprint para las rutas de usuario
users_routes = Blueprint('users_routes', __name__, url_prefix='/api')

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token faltante'}), 401
            try:
                token = token.split()[1]  # Bearer <token>
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.get(data['id'])
                if not current_user:
                    return jsonify({'message': 'Usuario no encontrado'}), 404
                if role and current_user.role != role:
                    return jsonify({'message': 'No autorizado'}), 403
            except Exception as e:
                return jsonify({'message': 'Token inválido', 'error': str(e)}), 401
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator


@users_routes.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'El email ya existe'}), 400
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user') # por defecto user
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado correctamente'}), 201


@users_routes.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    token = jwt.encode({
        'id': user.id_user,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        'token': token,
        'role': user.role,
        'username': user.username
    })

# Ruta para obtener todos los usuarios

@users_routes.route('/users', methods=['GET'])
@token_required(role="admin")
def get_users(current_user):
    users = User.query.all()
    if not users:
        return jsonify({'message': 'No hay usuarios registrados.'}), 200
    return jsonify([user.to_json() for user in users]), 200

# Ruta para obtener un usuario por su ID
@users_routes.route('/users/<string:id_user>', methods=['GET'])
@token_required()
def get_user(current_user, id_user):
    user = User.query.get(id_user)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    if current_user.id_user != id_user:          # propio usuario
        return jsonify({"error": "No autorizado"}), 403
    return jsonify(user.to_json()), 200


# Ruta para crear un nuevo usuario
@users_routes.route('/users/create', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validar que se proporcionen todos los campos necesarios
    if not data or not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Verificar si ya existe el email
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    role = data.get("role", "user")

    # Crear un nuevo usuario
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        role=role)

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

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        # Verificar que el nuevo email no esté ya en uso
        if User.query.filter_by(email=data["email"]).first() and user.email != data["email"]:
            return jsonify({"error": "El email ya está en uso"}), 400
        user.email = data["email"]
    if "password" in data:
        user.__init__(user.username, user.email, data["password"], user.role)  # Re-hashear password
    if "role" in data:
        user.role = data["role"]
        
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