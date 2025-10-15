from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    # Construir la URI de conexión a la base de datos MySQL
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT','3306')}/{os.getenv('MYSQL_DATABASE')}"
    # Desactivar el seguimiento de modificaciones
    SQLALCHEMY_TRACK_MODIFICATIONS = False
