from flask import Flask
from config.db import db
from config.config import Config
from routes.user_routes import users_bp
from routes.location_routes import locations_bp
from routes.rating_routes import ratings_bp
from routes.plate_routes import plates_bp
from flask_migrate import Migrate

# Crear la instancia de Flask
app = Flask(__name__)
# Configurar la URI de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
# Desactivar el seguimiento de modificaciones
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Registrar el blueprint de rutas de usuarios
app.register_blueprint(users_routes)
app.register_blueprint(locations_routes)

# Inicializar la extensión SQLAlchemy con la aplicación
db.init_app(app)

# Crear las tablas en la base de datos
with app.app_context():
    from models.user import User
    from models.location import Location
    from models.rating import Rating
    from models.plate import Plate
    db.create_all()

# Ejecutar la aplicación en modo debug
if __name__ == '__main__':
    app.run(debug=True)