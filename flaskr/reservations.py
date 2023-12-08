from flask import (Blueprint, render_template, request)
from flaskr.db import get_db
from flaskr.auth import login_required

reservations = Blueprint('reservations', __name__, url_prefix='/reservations')


@reservations.route('/unapproved',  methods=['GET', 'POST'])
@login_required
def get_unapproved_reservations():
    db = get_db()
    if request.method == 'POST':
        if 'approve' in request.form:
            if request.form['approve'] == 'Approve':
                    # approve reservations
                    reservation_id = request.form['reservation_id']
                    db.execute('UPDATE Reservation SET Approved_YN = "Y" WHERE id = ?', (reservation_id,))
                    db.commit()
                    print("approve")
        elif request.form['deny'] == 'Deny':
            # deny reservations
            reservation_id = request.form['reservation_id']
            db.execute('DELETE FROM Reservation WHERE id = ?', (reservation_id,))
            db.commit()
            print("deny")
    else:
        reservations_info = get_reservations('N')
        print(reservations_info)
    return render_template('reservations/unapproved.html', reservations_info=reservations_info)


@reservations.route('/approved', methods=['GET'])
@login_required
def get_approved_reservations():
    reservations_info = get_reservations('Y')
    return render_template('reservations/approved.html', reservations_info=reservations_info)


# get all reservations from database approved or unapproved
def get_reservations(approved):
    # connect to database
    db = get_db()
    # list passed to template
    reservations_info = [] 
    # get all reservations
    reservations = db.execute('SELECT * FROM Reservation WHERE Approved_YN =?',(approved)).fetchall()
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
        reservation_dict['id'] = reservation['id']
        reservation_dict['room_name'] = room_name['name']
        reservation_dict['res_date'] = date
        reservation_dict['beg_time'] = beg_time
        reservation_dict['end_time'] = end_time
        reservation_dict['purpose'] = purpose
        reservations_info.append(reservation_dict)
        return reservations_info