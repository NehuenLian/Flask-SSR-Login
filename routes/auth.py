from flask import Blueprint, render_template, redirect, url_for, session
from extensions import db, ph
from models.user import User
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from argon2.exceptions import VerifyMismatchError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        user = User.query.filter_by(username=username).first()

        if user is None:
            return render_template('login.html', form=form, error="Usuario o contraseña incorrectos.")

        try:
            print("Hash DB:", user['password'])
            print("Password ingresado:", password)

            ph.verify(user['password'], password)
            session.clear()
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        except VerifyMismatchError:
            return render_template('login.html', form=form, error="Usuario o contraseña incorrectos.")

    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            return render_template('register.html', form=form, error="El usuario ya existe.")

        hashed_password = ph.hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))