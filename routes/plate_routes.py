from flask import Blueprint, request, session, redirect, url_for, flash, render_template, current_app
from config.db import db
from models.plate import Plate
from models.location import Location
from utils.authentication import login_required, role_required
from werkzeug.utils import secure_filename
import os

plates_bp = Blueprint('plates', __name__, url_prefix='/plates')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@plates_bp.route('/create/<id_location>', methods=['GET', 'POST'])
@login_required
@role_required('owner')
def create_plate(id_location):
    location = Location.query.get_or_404(id_location)

    # dueño del local
    if session['user_id'] != location.id_user:
        flash('No tienes permiso para agregar platos a este local.', 'danger')
        return redirect(url_for('plates.list_plates'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        price = float(request.form['price'])

        # imagen
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'static', 'img', 'plates')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
        else:
            filename = 'no_image.png' # imagen por defecto

        new_plate = Plate(
            name=name,
            description=description,
            price=price,
            id_location=id_location,
            image=filename
        )
        db.session.add(new_plate)
        db.session.commit()

        flash('Plato agregado correctamente.', 'success')
        return redirect(url_for('locations.view_location', id_location=id_location))

    return render_template('plates/create.html', location=location)

@plates_bp.route('/edit/<id_plate>', methods=['GET', 'POST'])
@login_required
@role_required('owner')
def edit_plate(id_plate):
    plate = Plate.query.get_or_404(id_plate)
    location = plate.location  # relación desde el modelo Plate

    if session['user_id'] != location.id_user:
        flash('No tienes permiso para editar este plato.', 'danger')
        return redirect(url_for('plates.list_plates'))

    if request.method == 'POST':
        plate.name = request.form['name']
        plate.description = request.form.get('description')
        plate.price = float(request.form['price'])

        # nueva imagen
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'static', 'img', 'plates')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
            plate.image = filename

        db.session.commit()
        flash('Plato actualizado correctamente.', 'success')

        return redirect(url_for('locations.view_location', id_location=location.id_location))

    return render_template('plates/edit.html', plate=plate)

@plates_bp.route('/delete/<id_plate>', methods=['POST'])
@login_required
@role_required('owner')
def delete_plate(id_plate):
    plate = Plate.query.get_or_404(id_plate)
    location = plate.location

    if session['user_id'] != location.id_user:
        flash('No tienes permiso para eliminar este plato.', 'danger')
        return redirect(url_for('plates.list_plates'))

    db.session.delete(plate)
    db.session.commit()
    flash('Plato eliminado correctamente.', 'info')
    return redirect(url_for('locations.view_location', id_location=location.id_location))