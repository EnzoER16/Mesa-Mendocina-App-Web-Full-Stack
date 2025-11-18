from flask import Blueprint, request, session, redirect, url_for, flash, render_template, current_app
from config.db import db
from models.location import Location
from utils.authentication import login_required, role_required
from werkzeug.utils import secure_filename
import os

locations_bp = Blueprint('locations', __name__, url_prefix='/locations')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@locations_bp.route('/')
def list_locations():
    locations = Location.query.all()
    return render_template('locations/list.html', locations=locations)

@locations_bp.route('/<id_location>')
@login_required
def view_location(id_location):
    location = Location.query.get_or_404(id_location)
    return render_template('locations/view.html', location=location)

@locations_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('owner')
def create_location():

    departments = [
        "Capital", "Godoy Cruz", "Guaymallén", "Las Heras", "Lavalle", "Luján de Cuyo",
        "Maipú", "San Martín", "Rivadavia", "Junín", "Santa Rosa", "La Paz",
        "Tunuyán", "Tupungato", "San Carlos", "San Rafael", "General Alvear", "Malargüe"
        ]

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        department = request.form['department']
        phone = request.form['phone']
        description = request.form.get('description')
        id_user = session['user_id']

        # imagen
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'static', 'img', 'locations')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
        else:
            filename = 'no_image.png' # imagen por defecto

        # telefono distinto
        existing_location = Location.query.filter_by(phone=phone).first()
        if existing_location:
            flash('Este número de teléfono ya está registrado.', 'danger')
            return redirect(url_for('locations.create_location'))

        new_location = Location(
            name=name,
            address=address,
            department=department,
            phone=phone,
            id_user=id_user,
            description=description,
            image=filename
        )
        db.session.add(new_location)
        db.session.commit()
        flash('Ubicación creada correctamente.', 'success')
        return redirect(url_for('locations.list_locations'))

    return render_template('locations/create.html', departments=departments)

@locations_bp.route('/edit/<id_location>', methods=['GET', 'POST'])
@login_required
@role_required('owner')
def edit_location(id_location):
    location = Location.query.get_or_404(id_location)

    if session['user_id'] != location.id_user:
        flash('No tienes permiso para editar esta ubicación.', 'danger')
        return redirect(url_for('locations.list_locations'))

    if request.method == 'POST':
        location.name = request.form['name']
        location.address = request.form['address']
        location.department = request.form['department']
        location.phone = request.form['phone']
        location.description = request.form.get('description')

        # imagen
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'static', 'img', 'locations')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))

            # borrar la imagen anterior si no era la de por defecto
            if location.image and location.image != 'no_image.png':
                old_path = os.path.join(upload_path, location.image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            location.image = filename
        # si no se sube nada se mantiene la imagen existente

        db.session.commit()
        flash('Ubicación actualizada correctamente.', 'success')
        return redirect(url_for('locations.view_location', id_location=location.id_location))

    return render_template('locations/edit.html', location=location)

@locations_bp.route('/delete/<id_location>', methods=['POST'])
@login_required
@role_required('owner')
def delete_location(id_location):
    location = Location.query.get_or_404(id_location)

    if session['user_id'] != location.id_user:
        flash('No tienes permiso para eliminar esta ubicación.', 'danger')
        return redirect(url_for('locations.list_locations'))

    db.session.delete(location)
    db.session.commit()
    flash('Ubicación eliminada correctamente.', 'info')
    return redirect(url_for('locations.list_locations'))