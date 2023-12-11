from flask import (Blueprint, render_template, request, url_for, redirect)
from flaskr.db import get_db
from flaskr.auth import login_required

reservations = Blueprint('reservations', __name__, url_prefix='/reservations')



@reservations.route('/pending',  methods=['GET', 'POST'])
@login_required
def pending():
    db = get_db()
    if request.method == 'POST':
        if 'approve' in request.form:
            if request.form['approve'] == 'Approve':
                    # approve reservations
                    reservation_id = request.form['reservation_id']
                    db.execute('UPDATE Reservation SET Approved_YN = "Y" WHERE id = ?', (reservation_id,))
                    db.commit()
                    print("approve")
        elif 'cancel' in request.form:
            if request.form['cancel'] == 'Cancel':
                # cancel reservations
                reservation_id = request.form['reservation_id']
                db.execute('DELETE FROM Reservation WHERE id = ?', (reservation_id,))
                db.commit()
                print("cancel")
        elif request.form['deny'] == 'Deny':
            # deny reservations
            reservation_id = request.form['reservation_id']
            db.execute('DELETE FROM Reservation WHERE id = ?', (reservation_id,))
            db.commit()
            print("deny")
        return redirect(url_for('reservations.pending'))
    else:
        reservations_info = get_reservations('N')

        return render_template('reservations/pending.html', reservations_info=reservations_info)


@reservations.route('/approved', methods=['GET', 'POST'])
@login_required
def approved():
    if request.method == 'POST':
        if 'cancel' in request.form:
            if request.form['cancel'] == 'Cancel':
                # cancel reservations
                reservation_id = request.form['reservation_id']
                db = get_db()
                db.execute('DELETE FROM Reservation WHERE id = ?', (reservation_id,))
                db.commit()
                print("cancel")
        return redirect(url_for('reservations.approved'))

    reservations_info = get_reservations('Y')
    return render_template('reservations/approved.html', reservations_info=reservations_info)


# get all reservations from database approved or pending
def get_reservations(approved, user_id=None):
    # connect to database
    db = get_db()
    # list passed to template
    reservations_info = [] 
    # get all reservations
    if user_id is None:
        reservations = db.execute('SELECT * FROM Reservation WHERE Approved_YN =?',(approved)).fetchall()
    else:
        reservations = db.execute('SELECT * FROM Reservation WHERE Approved_YN = ? AND User_Id = ?',(approved, user_id)).fetchall()
    # loop through all reservations
    for reservation in reservations:

        reservation_dict = {}

        # get first name and last name of each user who made a reservation
        user_name = db.execute('SELECT first_name, last_name FROM User WHERE id = ?', (reservation['user_id'],)).fetchone()

        # get picture_name of each reservation
        picture_name = db.execute('SELECT picture_name FROM Room WHERE id = ?', (reservation['room_id'],)).fetchone()

        # get room name and room number of each reservation
        room_name = db.execute('SELECT name FROM Room WHERE id = ?', (reservation['room_id'],)).fetchone()

        # get organization name of each reservation
        org_name = db.execute('SELECT Name FROM Organization WHERE Id = ?', (reservation['Organization_Id'],)).fetchone()

        if org_name is not None:
            reservation_dict['org_name'] = org_name['org_name']
        # add all info to dictionary
        reservation_dict['user_name'] = user_name['first_name'] + ' ' + user_name['last_name']
        reservation_dict['picture_name'] = picture_name['picture_name']
        reservation_dict['id'] = reservation['id']
        reservation_dict['room_id'] = reservation['room_id']
        reservation_dict['room_name'] = room_name['name']
        reservation_dict['res_date'] = reservation['res_date']
        reservation_dict['beg_time'] = reservation['beg_time']
        reservation_dict['end_time'] = reservation['end_time']
        reservation_dict['purpose'] = reservation['purpose']
        # add dictionary to list
        reservations_info.append(reservation_dict)

    return reservations_info


