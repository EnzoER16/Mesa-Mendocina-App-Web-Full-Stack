from flask import Flask, render_template, redirect, url_for, request, session
from config.db import db
from config.config import Config
from routes.user_routes import users_bp
from routes.location_routes import locations_bp
from routes.plate_routes import plates_bp
from routes.rating_routes import ratings_bp
from models.user import User
from models.location import Location
from models.plate import Plate
from models.rating import Rating
from werkzeug.security import check_password_hash, generate_password_hash

# Crear la instancia de Flask
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY  # Para session

# Configurar la app usando la clase Config
app.config.from_object(Config)

# Registrar blueprints
app.register_blueprint(users_bp)
app.register_blueprint(locations_bp)
app.register_blueprint(plates_bp)
app.register_blueprint(ratings_bp)

# Inicializar la extensión SQLAlchemy
db.init_app(app)

# Crear tablas
with app.app_context():
    db.create_all()

# --------------------------
# RUTAS FRONTEND
# --------------------------


@app.route('/')
def index():
    locations = Location.query.all()
    featured_plates = Plate.query.limit(5).all()  # ejemplo: 5 destacados
    return render_template('index.html', locations=locations, featured_plates=featured_plates, session=session)


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id_user
            session['username'] = user.username
            session['role'] = user.role
            session['email'] = user.email
            return redirect(url_for('user_menu'))
        else:
            return render_template('login.html', error="Credenciales inválidas")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error="El email ya existe")
        new_user = User(username=username, email=email,
                        password=password, role='user')
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id_user
        session['username'] = new_user.username
        session['role'] = new_user.role
        session['email'] = new_user.email
        return redirect(url_for('user_menu'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/user/menu')
def user_menu():
    if 'user_id' not in session:
        return redirect(url_for('login_view'))

    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login_view'))

    # Revisar si tiene local registrado y actualizar rol a owner
    user_locations = Location.query.filter_by(id_user=user.id_user).all()
    if user_locations and user.role != 'owner':
        user.role = 'owner'
        db.session.commit()
        session['role'] = 'owner'

    if user.role == 'owner':
        return render_template('perfil_owner.html', username=user.username)
    else:
        return render_template('perfil_user.html', username=user.username)


@app.route('/user/register_location', methods=['GET', 'POST'])
def register_location():
    if 'user_id' not in session:
        return redirect(url_for('login_view'))
    if session.get('role') != 'owner' and request.method == 'GET':
        # mostrar formulario de registro para usuarios que aún no son owner
        return render_template('register_location.html')

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        department = request.form['department']
        schedule = request.form['schedule']
        price_range = request.form['price_range']
        phone = request.form['phone']

        new_location = Location(
            name=name,
            address=address,
            department=department,
            schedule=schedule,
            price_range=price_range,
            phone=phone,
            id_user=session['user_id']
        )
        db.session.add(new_location)
        db.session.commit()

        # Actualizar rol a owner
        user = User.query.get(session['user_id'])
        user.role = 'owner'
        db.session.commit()
        session['role'] = 'owner'

        return redirect(url_for('user_menu'))

    return render_template('register_location.html')


@app.route('/user/load_plates', methods=['GET', 'POST'])
def load_plates():
    if 'user_id' not in session:
        return redirect(url_for('login_view'))
    if session.get('role') != 'owner':
        return "No autorizado", 403

    user_locations = Location.query.filter_by(id_user=session['user_id']).all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        id_location = request.form['id_location']
        new_plate = Plate(name=name, description=description,
                          price=price, id_location=id_location)
        db.session.add(new_plate)
        db.session.commit()
        return redirect(url_for('user_menu'))

    return render_template('load_plates.html', locations=user_locations)


# --------------------------
# Ejecutar app
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)
