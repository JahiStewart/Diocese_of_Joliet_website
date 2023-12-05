from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flaskr.db import get_db
from flaskr.auth import login_required

reservations = Blueprint('reservations', __name__, url_prefix='/reservations')


@reservations.route('/all')
def get_all_reservations():
    db = get_db()

    # list passed to template
    reservations_list = []

    # get all reservations
    reservations = db.execute('SELECT * FROM Reservation').fetchall()

    # loop through all reservations
    for reservation in reservations:
        
        reservation_dict = {}

        # get first name and last name of each user who made a reservation
        user_name = db.execute('SELECT first_name, last_name FROM User WHERE id = ?', (reservation['user_id'],)).fetchone()
        # get picture_name of each reservation
        picture_name = db.execute('SELECT picture_name FROM Room WHERE id = ?', (reservation['room_id'],)).fetchone()
        # get room_name of each reservation
        room_name = db.execute('SELECT name FROM Room WHERE id = ?', (reservation['room_id'],)).fetchone()
        date = reservation['res_date']
        beg_time = reservation['beg_time']
        end_time = reservation['end_time']
        purpose = reservation['purpose']
        reservation_dict['user_name'] = user_name['first_name'] + ' ' + user_name['last_name']
        reservation_dict['picture_name'] = picture_name['picture_name']
        reservation_dict['room_name'] = room_name['name']
        reservation_dict['res_date'] = date
        reservation_dict['beg_time'] = beg_time
        reservation_dict['end_time'] = end_time
        reservation_dict['purpose'] = purpose
        reservations_list.append(reservation_dict)

    return render_template('reservations/all.html', reservations_list=reservations_list)
