import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4

from flaskr.db import get_db

auth = Blueprint('auth', __name__, url_prefix='/auth')

# creates the register view (register new user)
@auth.route('/register', methods=('GET', 'POST'))
def register():
    error = None
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
            user_id = str(uuid4())
            try:
                db.execute(
                    "INSERT INTO user (Id, Email, Password, First_Name, Last_Name, Phone) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id,email,generate_password_hash(password),fname,lname,phone),
                )
                db.commit()

                # TESTING PURPOSES (REMOVE LATER)
                new_user = db.execute(
                    "SELECT * FROM user WHERE email = ?", (email,)
                ).fetchone()
                print("New User:", new_user['First_Name'], new_user['Last_Name'], new_user['email'], new_user['phone'])

            # catch duplicate email error
            except db.IntegrityError:
                error = f"Email {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', error=error)


# creates the login view (login existing user)
@auth.route('/login', methods=('GET', 'POST'))
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
            return redirect(url_for('form.index'))

        flash(error)

    return render_template('auth/login.html', error=error)

# checks if user is logged in (if user_id is stored in the session, 
#                              then it stores user data in g.user)
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# log out user
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('form.index'))


# function that requires user to be logged
# use this to decorate views that require the user to be logged in
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@auth.route('/myaccount')
def myaccount():
    # create connection to database
    db = get_db()
    # get current users id
    user_id = session.get('user_id')
    # get users organization if any
    org = db.execute(
        'SELECT * FROM organization WHERE id = ?',
        (user_id,)
    ).fetchone()
    # catch error in case user has no organization
    try:
        org_name = org['name']
    except:
        org_name = "You currenlty don't belong to any organizations."

    return render_template('auth/myaccount.html', org_name=org_name)
