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
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app,db)

app.register_blueprint(users_bp)
app.register_blueprint(locations_bp)
app.register_blueprint(ratings_bp)
app.register_blueprint(plates_bp)

# Ejecutar la aplicación en modo debug
if __name__ == '__main__':
    app.run(debug=True)