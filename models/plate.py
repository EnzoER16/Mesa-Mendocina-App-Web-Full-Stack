from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from config.db import db
from models.rating import Rating
from models.location import Location
from utils.authentication import login_required

ratings_bp = Blueprint('ratings', __name__, url_prefix='/ratings')

@ratings_bp.route('/my_ratings')
@login_required
def view():
    if session.get('role') != 'user':
        flash('No tienes permiso para acceder a esta sección.', 'danger')
        return redirect(url_for('public'))  # o a otra página segura

    id_user = session['user_id']
    ratings = Rating.query.filter_by(id_user=id_user).all()
    return render_template('ratings/view.html', ratings=ratings)

@ratings_bp.route('/edit/<id_rating>', methods=['GET', 'POST'])
@login_required
def edit_rating(id_rating):
    rating = Rating.query.get_or_404(id_rating)

    # mismo usuario
    if session['user_id'] != rating.id_user:
        flash('No tienes permiso para editar esta reseña.', 'danger')
        return redirect(url_for('ratings.list_ratings', id_location=rating.id_location))

    if request.method == 'POST':
        rating.rate = int(request.form['rate'])
        rating.comment = request.form.get('comment')
        db.session.commit()
        flash('Reseña actualizada correctamente.', 'success')
        return redirect(url_for('ratings.list_ratings', id_location=rating.id_location))

    return render_template('ratings/edit.html', rating=rating)

@ratings_bp.route('/location/<id_location>')
def list_ratings(id_location):
    location = Location.query.get_or_404(id_location)
    ratings = Rating.query.filter_by(id_location=id_location).all()
    return render_template('ratings/list.html', location=location, ratings=ratings)

@ratings_bp.route('/create/<id_location>', methods=['GET', 'POST'])
@login_required
def create_rating(id_location):
    location = Location.query.get_or_404(id_location)
    id_user = session['user_id']

    if request.method == 'POST':
        rate = int(request.form['rate'])
        comment = request.form.get('comment')

        # una reseña por local
        existing = Rating.query.filter_by(id_user=id_user, id_location=id_location).first()
        if existing:
            flash('Ya has calificado este local.', 'warning')
            return redirect(url_for('ratings.list_ratings', id_location=id_location))

        new_rating = Rating(rate=rate, comment=comment, id_user=id_user, id_location=id_location)
        db.session.add(new_rating)
        db.session.commit()
        flash('Calificación enviada correctamente.', 'success')
        return redirect(url_for('ratings.list_ratings', id_location=id_location))

    return render_template('ratings/create.html', location=location)

@ratings_bp.route('/delete/<id_rating>', methods=['POST'])
@login_required
def delete_rating(id_rating):
    rating = Rating.query.get_or_404(id_rating)
    if session['user_id'] != rating.id_user:
        flash('No tienes permiso para eliminar esta reseña.', 'danger')
        return redirect(url_for('ratings.list_ratings', id_location=rating.id_location))

    db.session.delete(rating)
    db.session.commit()
    flash('Reseña eliminada correctamente.', 'info')
    return redirect(url_for('ratings.list_ratings', id_location=rating.id_location))