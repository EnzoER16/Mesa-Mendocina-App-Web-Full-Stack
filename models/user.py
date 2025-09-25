from werkzeug.security import generate_password_hash, check_password_hash
from config.db import db
import uuid

class User(db.Model):
    # Nombre de la tabla en la base de datos
    __tablename__ = 'users'
    
    # Definición de las columnas de la tabla
    id_user = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user') # 'user' o 'owner'

    # Constructor de la clase User
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    # Verificar la contraseña del usuario
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Convertir el modelo a formato JSON
    def to_json(self):
        return {
            'id_user': self.id_user,
            'username': self.name,
            'email': self.email,
            'role': self.role
        }
    
    #to do: verificar el email