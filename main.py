from flask import Flask
from config.db import db
from config.config import DATABASE_CONNECTION_URI

# Crear la instancia de Flask
app = Flask(__name__)
# Configurar la URI de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
# Desactivar el seguimiento de modificaciones
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la extensión SQLAlchemy con la aplicación
db.init_app(app)

# Ejecutar la aplicación en modo debug
if __name__ == '__main__':
    app.run(debug=True)