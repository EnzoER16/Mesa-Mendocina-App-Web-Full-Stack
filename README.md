# Mesa-Mendocina-App-Web-Full-Stack

## Descripción de la problemática
Mesa Mendocina es una aplicación web que permite visibilizar, promocionar y difundir locales gastronómicos que ofrecen comida típica mendocina.
Su objetivo es facilitar a usuarios locales y turistas el acceso a información confiable sobre dichos locales, así como permitir a los dueños gestionar su presencia digital.

## Integrantes del grupo
- Enzo Rojas
- Matías Agüero
- Gustavo Vera
- Lautaro Videla

## Entidades principales
- Usuario (User): Representa a los clientes o dueños.
- Local (Location): Local gastronómico registrado por un dueño.
- Valoracion (Rating): Reseña y puntaje que un cliente deja sobre un local.
- Plato (Plate): Plato que se sirve en un local.
- Reserva (Reservation): Reserva realizada por un cliente en un local.

## Diagrama de la base de datos
![Diagrama de la base de datos](diagram.png)

## Capturas de pantalla

### Página de inicio
![Página de inicio](screenshots/homepage.png)

### Registro de usuario
![Registro de usuario](screenshots/register.png)

### Perfil de usuario
![Perfil de usuario](screenshots/user_profile.png)

### Lista de locales
![Lista de locales](screenshots/location_list.png)

### Detalle de local
![Detalle de local](screenshots/location_detail.png)

### Gestión de reservas
![Gestión de reservas](screenshots/reservation_management.png)

## Instalación y configuración

1. Clonar el proyecto:

```sh
git clone https://https://github.com/EnzoER16/Mesa-Mendocina-App-Web-Full-Stack
```

2. Crear entorno virtual:

· Windows:

```sh
python -m venv <environment_name>
```

· Linux/macOS:

```sh
python3 -m venv <environment_name>
```

3. Activar entorno virtual:

· Windows:

```sh
<environment_name>\scripts\activate
```

· Linux / macOS:

```sh
source <environment_name>/bin/activate
```

4. Instalar dependencias:

```sh
pip install -r requirements.txt
```

5. Configurar variables de entorno:
Crear un archivo `.env` en la raíz del proyecto y definir las siguientes variables:

```sh
MYSQL_USER=XXXX
MYSQL_PASSWORD=XXXX
MYSQL_HOST=XXXX
MYSQL_DATABASE=XXXX
MYSQL_PORT=XXXX
JWT_SECRET=XXXX
```

6. Ejecutar migraciones de la base de datos:

Inicializar migraciones

```sh
flask db init
```

Generar la migración inicial

```sh
flask db migrate -m "Inicialización de tablas"
```

Aplicar cambios a la base de datos

```sh
flask db upgrade
```

7. Ejecutar la aplicación

```sh
flask run
```

## Documentación adicional
- Framework backend: Flask
- ORM: SQLAlchemy
- Migraciones: Flask-Migrate
- Frontend: HTML, CSS, Bootstrap, JS
- Base de datos: MySQL
- Variables de entorno: python-dotenv