from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from config.db import db
from models.reservation import Reservation
from models.location import Location
from utils.authentication import login_required, role_required
import datetime

reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@reservations_bp.route('/')
@login_required
def list_reservations():
    if session['role'] == 'owner':
        owner_locations = Location.query.filter_by(id_user=session['user_id']).all()
        location_ids = [loc.id_location for loc in owner_locations]
        reservations = Reservation.query.filter(Reservation.id_location.in_(location_ids)).all()
    else:
        user_id = session['user_id']
        reservations = Reservation.query.filter_by(id_user=user_id).all()

    return render_template('reservations/list.html', reservations=reservations)

@reservations_bp.route('/edit/<id_reservation>', methods=['GET', 'POST'])
@login_required
def edit_reservation(id_reservation):
    reservation = Reservation.query.get_or_404(id_reservation)

    # mismo usuario
    if session['user_id'] != reservation.id_user:
        flash('No tienes permiso para editar esta reservación.', 'danger')
        return redirect(url_for('reservations.list_reservations'))

    # no editar si es aceptada, rechazada o cancelada
    if reservation.status in ['accepted', 'rejected', 'cancelled']:
        flash('No puedes editar una reservación que ya fue procesada.', 'warning')
        return redirect(url_for('reservations.view_reservation', id_reservation=id_reservation))

    if request.method == 'POST':
        reservation.date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        reservation.time = datetime.datetime.strptime(request.form['time'], '%H:%M').time()
        reservation.people = int(request.form['people'])
        db.session.commit()
        flash('Reservación actualizada correctamente.', 'success')
        return redirect(url_for('reservations.view_reservation', id_reservation=id_reservation))

    return render_template('reservations/edit.html', reservation=reservation)

@reservations_bp.route('/cancel/<id_reservation>', methods=['POST'])
@login_required
def cancel_reservation(id_reservation):
    reservation = Reservation.query.get_or_404(id_reservation)

    # mismo usuario
    if session['user_id'] != reservation.id_user:
        flash('No tienes permiso para cancelar esta reservación.', 'danger')
        return redirect(url_for('reservations.list_reservations'))

    # cancelar si es pendiente o aceptada
    if reservation.status not in ['pending', 'accepted']:
        flash('No puedes cancelar una reservación que ya fue rechazada o cancelada.', 'warning')
        return redirect(url_for('reservations.view_reservation', id_reservation=id_reservation))

    reservation.status = 'cancelled'
    db.session.commit()
    flash('Reservación cancelada correctamente.', 'info')
    return redirect(url_for('reservations.list_reservations'))

@reservations_bp.route('/create/<id_location>', methods=['GET', 'POST'])
@login_required
def create_reservation(id_location):
    if session['role'] == 'owner':
        flash('Los owners no pueden hacer reservas.', 'danger')
        return redirect(url_for('reservations.list_reservations'))

    location = Location.query.get_or_404(id_location)
    id_user = session['user_id']

    if request.method == 'POST':
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time = datetime.datetime.strptime(request.form['time'], '%H:%M').time()
        people = int(request.form['people'])

        new_reservation = Reservation(
            date=date, time=time, people=people,
            id_user=id_user, id_location=id_location
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('Reservación creada correctamente.', 'success')
        return redirect(url_for('reservations.list_reservations'))

    return render_template('reservations/create.html', location=location)

@reservations_bp.route('/<id_reservation>')
@login_required
def view_reservation(id_reservation):
    reservation = Reservation.query.get_or_404(id_reservation)
    if session['user_id'] != reservation.id_user and session['role'] != 'owner':
        flash('No tienes permiso para ver esta reservación.', 'danger')
        return redirect(url_for('reservations.list_reservations'))
    return render_template('reservations/view.html', reservation=reservation)

@reservations_bp.route('/status/<id_reservation>/<status>', methods=['POST'])
@login_required
@role_required('owner')
def change_status(id_reservation, status):
    reservation = Reservation.query.get_or_404(id_reservation)
    if status not in ['accepted', 'rejected', 'cancelled']:
        flash('Estado inválido.', 'danger')
        return redirect(url_for('reservations.list_reservations'))
    reservation.status = status
    db.session.commit()
    flash(f'Reservación {status} correctamente.', 'success')
    return redirect(url_for('reservations.view_reservation', id_reservation=id_reservation))

@reservations_bp.route('/delete/<id_reservation>', methods=['POST'])
@login_required
def delete_reservation(id_reservation):
    reservation = Reservation.query.get_or_404(id_reservation)

    if session['user_id'] != reservation.id_user and session['role'] != 'owner':
        flash('No tienes permiso para eliminar esta reservación.', 'danger')
        return redirect(url_for('reservations.list_reservations'))

    db.session.delete(reservation)
    db.session.commit()
    flash('Reservación eliminada correctamente.', 'info')
    return redirect(url_for('reservations.list_reservations'))