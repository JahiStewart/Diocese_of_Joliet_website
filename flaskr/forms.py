from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SubmitField, DateField, RadioField, IntegerField, TimeField
from wtforms.validators import InputRequired, NumberRange
from flaskr.db import get_db
from uuid import uuid4
from flaskr.auth import login_required
from datetime import datetime

forms = Blueprint('form', __name__)

class RoomRequestForm(FlaskForm):
    date = DateField('Date', validators=[InputRequired()])
    start_time = TimeField('Start', validators=[InputRequired()])
    end_time = TimeField('End', validators=[InputRequired()])

    arrangement = RadioField('Room Arrangement:', choices=["", "", ""])

    purpose = StringField('Purpose:', validators=[InputRequired()])
    attendees = IntegerField('Number of Attendees', validators=[InputRequired(), NumberRange(min=1, message='Must be greater than 0')]) 

    coffee = BooleanField('Coffee')
    soda = BooleanField('Soda')
    water = BooleanField('Water')
    catering = BooleanField('Catering')

    lapel_mic = BooleanField('Lapel Microphone')
    podium_mic = BooleanField('Podium Microphone')
    handheld_mic = BooleanField('Handheld Microphone')
    conference_phone = BooleanField('Conference Phone')
    whiteboard = BooleanField('Whiteboard')
    easel = BooleanField('Easel')
    flipchart = BooleanField('Flipchart')

    notes = StringField('Special Notes or Setup Instructions:')

    no_lobby = BooleanField('Hide from lobby')

    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})
    submit = SubmitField('Submit')



@forms.route('/<string:room_id>/book', methods=['GET', 'POST'])
@login_required
def book(room_id):
    # get date, start time, end time, and attendees from session
    date = session.get('date')
    date = datetime.strptime(date, '%Y-%m-%d').date()
    start_time = datetime.strptime(session.get('start_time'), '%H:%M:%S').time()
    end_time = datetime.strptime(session.get('end_time'), '%H:%M:%S').time()
    attendees = session.get('attendees')

    # create form with date, start time, and end time pre-populated
    form = RoomRequestForm(date=date, start_time=start_time, end_time=end_time, attendees=attendees)

    db = get_db()

    # get chosen room from database
    room = db.execute('SELECT * FROM room WHERE Id = ?', (room_id,)).fetchone()

    # get room arrangement options if the room has them
    rooms_with_arrangements = ["506 and 507", "503", "504", "505"]  
    room_arrangements = []
    if room['Id'] in rooms_with_arrangements:
        room_arrangements = db.execute('SELECT * FROM RoomArrangement').fetchall()

    # get organizations that the user is a part of
    organizations = db.execute('SELECT Name, Id from Organization WHERE Id IN (SELECT Organization_Id from UserOrganization WHERE User_Id = ?)', (session.get('user_id'),)).fetchall()

    if request.method == 'POST':
        if form.cancel.data:  # if cancel button is clicked, the form.cancel.data will be True
            return redirect(url_for('form.index')) # go back to previous page (change to room select once that page exists)

        org_id = request.form.get('org_id')
        room_arrangement_id = request.form.get('arrangement')
        print("org_id:", org_id)
        print("room_arrangement_id:", room_arrangement_id)

        # export all of the data from this form into the database
        reservation_id = str(uuid4())
        db.execute(
            '''INSERT INTO Reservation 
            (Id, User_id, Res_Date, Beg_Time, End_Time, Purpose, Organization_Id, Attendee_Count, Coffee_YN, Soda_YN, 
            Water_YN, Catering_YN, Lapel_Mic, Podium_Mic, Handheld_Mic, Conf_Phone, Whiteboard_YN, Easel_YN, Special_Notes, Lobby_YN,
            Room_Id, RoomArrangement_Id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (reservation_id, session.get('user_id'), form.date.data, form.start_time.data.strftime('%H:%M:%S'), form.end_time.data.strftime('%H:%M:%S'), form.purpose.data, org_id, form.attendees.data, form.coffee.data, form.soda.data, 
            form.water.data, form.catering.data, form.lapel_mic.data, form.podium_mic.data, form.handheld_mic.data, form.conference_phone.data, form.whiteboard.data, form.easel.data, form.notes.data, form.no_lobby.data, 
            room_id, room_arrangement_id),)
        db.commit()
        return redirect(url_for('form.index')) # go back to previous page (change to confirmation page or myaccount page)
    else:
        return render_template('book.html', form=form, room=room, organizations=organizations, room_arrangements=room_arrangements)


# HOME PAGE - ROOM SEARCH FORM  
@forms.route('/', methods=['GET', 'POST'])
def index():
    form = RoomRequestForm()

    if request.method =='POST':

        # store date, start time, and end time in session
        session['date'] = form.date.data.strftime('%Y-%m-%d')
        session['start_time'] = form.start_time.data.strftime('%H:%M:%S')
        session['end_time'] = form.end_time.data.strftime('%H:%M:%S')
        session['attendees'] = form.attendees.data
        return redirect(url_for('form.results'))
        # return render_template('index.html', form=form) 
    
    else:
        return render_template('index.html', form=form)


# RESULTS PAGE - SHOWS AVAILABLE ROOMS
@forms.route('/results', methods=['GET', 'POST'])
def results():

    if request.method == 'POST':
        room_id = request.form.get('room_Id')
        return redirect(url_for('form.book', room_id=room_id))
    
    else:
        # get date, start time, and end time from session
        date = session.get('date')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        start_time = datetime.strptime(session.get('start_time'), '%H:%M:%S').time()
        end_time = datetime.strptime(session.get('end_time'), '%H:%M:%S').time()
        attendees = session.get('attendees')

        # create form with date, start time, and end time pre-populated
        form = RoomRequestForm(date=date, start_time=start_time, end_time=end_time, attendees=attendees)

        # get results from database
        results = get_results(form.attendees.data, form.date.data, form.start_time.data, form.end_time.data)
        # results = []
        return render_template('results.html', form=form, results=results)


def get_results(attendees,date, start_time, end_time):
    db = get_db()

    # get all rooms that are not reserved during the specified time
    available_rooms = db.execute('''SELECT * FROM Room WHERE Id NOT IN 
                                 (SELECT room_id FROM reservation WHERE Res_Date = ?)''',(date,)).fetchall()
    
    return available_rooms

# AND (Beg_Time >= ? AND Beg_Time <= ?
#                                  OR End_Time >= ? AND End_Time <= ?
#                                  OR Beg_Time <= ? AND End_Time >= ?)

#                                  , start_time, end_time, start_time, end_time, start_time, end_time