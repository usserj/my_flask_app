from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from . import user_bp
from .forms import LoginForm, RegistrationForm
from .models import User, Role
from my_flask_app.extensions import db


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('user.home'))
        flash('Credenciales inválidas', 'danger')
    return render_template('login.html', form=form, title='Iniciar Sesión')


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('user.login'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            identification=form.identification.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data,
        )
        user.set_password(form.password.data)
        # Assign default role 'Paciente'
        role = Role.query.filter_by(name='Paciente').first()
        if role:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado con éxito.', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form, title='Registro')


@user_bp.route('/')
def home():
    return render_template('home.html')
