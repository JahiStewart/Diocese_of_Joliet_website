import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# creates the register view (register new user)
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # request user input (first name, last name, email, password, phone number) via POST
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        # create database connection
        db = get_db()
        error = None

        # catch empty fields
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        # if no errors, insert new user into database
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (fname, lname, email, password, phone) VALUES (?, ?, ?, ?, ?)",
                    (fname, lname, email, generate_password_hash(password), phone),
                )
                db.commit()

                # TESTING PURPOSES (REMOVE LATER)
                new_user = db.execute(
                    "SELECT * FROM user WHERE email = ?", (email,)
                ).fetchone()
                print("New User:", new_user['fname'], new_user['lname'], new_user['email'], new_user['phone'])

            # catch duplicate email error
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# creates the login view (login existing user)
@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', error=error)

# checks if user is logged in (if user_id is stored in the session, 
#                              if so, then it stores user data in g.user)
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# log out user
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
