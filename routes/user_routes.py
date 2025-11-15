from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from config.db import db
from models.user import User
from werkzeug.security import generate_password_hash
from utils.authentication import login_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/auth/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('users.user_register'))
        
        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. ¡Bienvenido a Mesa Mendocina!', 'success')
        return redirect(url_for('users.user_login'))
    
    return render_template('users/register.html')

@users_bp.route('/auth/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id_user
            session['username'] = user.username
            session['role'] = user.role

            # flash(f'Bienvenido, {user.username}!', 'success')
            return redirect(url_for('private'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
            return redirect(url_for('users.user_login'))
    
    return render_template('users/login.html')

@users_bp.route('/logout')
@login_required
def user_logout():
    session.clear()
    # flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('public'))

@users_bp.route('/<id_user>')
@login_required
def view_user(id_user):
    user = User.query.get_or_404(id_user)
    if session['user_id'] != user.id_user:
        flash('No tienes permiso para ver este perfil.', 'danger')
        return redirect(url_for('private'))
    return render_template('users/view.html', user=user)

@users_bp.route('/edit/<id_user>', methods=['GET', 'POST'])
@login_required
def edit_user(id_user):
    user = User.query.get_or_404(id_user)
    if session.get('user_id') != user.id_user:
        flash('No tienes permiso para editar este perfil.', 'danger')
        return redirect(url_for('private'))

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        password = request.form.get('password')

        if password:
            user.password_hash = generate_password_hash(password)

        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('users.view_user', id_user=user.id_user))
    
    return render_template('users/edit.html', user=user)

@users_bp.route('/delete/<id_user>', methods=['POST'])
@login_required
def delete_user(id_user):
    user = User.query.get_or_404(id_user)
    if session['user_id'] != user.id_user:
        flash('No tienes permiso para eliminar este perfil.', 'danger')
        return redirect(url_for('private'))

    db.session.delete(user)
    db.session.commit()

    # cerrar sesion si se elimina la cuenta
    if session.get('user_id') == id_user:
        session.clear()
        flash('Tu cuenta ha sido eliminada.', 'info')
        return redirect(url_for('public'))
    
    flash('Usuario eliminado correctamente.', 'info')
    return redirect(url_for('private'))