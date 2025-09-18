from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Obtener las variables de entorno necesarias para la conexión a la base de datos
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DB")
port = os.getenv("MYSQL_PORT", "3306")

# Construir la URI de conexión a la base de datos MySQL
DATABASE_CONNECTION_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"