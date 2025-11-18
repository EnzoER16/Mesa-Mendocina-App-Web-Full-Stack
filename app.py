from flask import Flask, render_template, redirect, url_for, session
from config.db import db
from config.config import Config
from routes.user_routes import users_bp
from routes.location_routes import locations_bp
from routes.rating_routes import ratings_bp
from routes.plate_routes import plates_bp
from routes.reservation_routes import reservations_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(users_bp)
app.register_blueprint(locations_bp)
app.register_blueprint(ratings_bp)
app.register_blueprint(plates_bp)
app.register_blueprint(reservations_bp)

@app.route('/')
def public():
    locations = Location.query.all()
    if session.get('user_id'):
        return redirect(url_for('private'))
    return render_template('public.html', locations=locations)

@app.route('/index')
def private():
    if not session.get('user_id'):
        return redirect(url_for('public'))
    locations = Location.query.all()
    return render_template('locations/list.html', locations=locations)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    with app.app_context():
        from models.user import User
        from models.location import Location
        from models.plate import Plate
        from models.rating import Rating
        from models.reservation import Reservation
        db.create_all()
    app.run(debug=True)