from flask import Blueprint, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SubmitField, DateField, RadioField
from wtforms.validators import InputRequired
from flaskr.db import get_db
from uuid import uuid4

forms = Blueprint('form', __name__)

class RoomRequestForm(FlaskForm):

    date = DateField('', validators=[InputRequired()])
    start_time = SelectField('', choices=['06:00 AM', '06:30 AM', '07:00 AM', '07:30 AM', '08:00 AM', '08:30 AM', '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM', '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM', '06:30 PM', '07:00 PM', '07:30 PM', '08:00 PM'])
    end_time = SelectField('', choices=['06:00 AM', '06:30 AM', '07:00 AM', '07:30 AM', '08:00 AM', '08:30 AM', '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM', '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM', '06:30 PM', '07:00 PM', '07:30 PM', '08:00 PM'])

    arrangement = RadioField('Room Arrangement:', choices=["", "", ""])

    purpose = StringField('Purpose:', validators=[InputRequired()])
    attendees = SelectField('Number of Attendees', choices=["",1,2,3,4,5,6,7,8,9,10], validators=[InputRequired()]) # make a function to pull the values in the array from the max occupancy of the room 

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


@forms.route('/wtf', methods=['GET', 'POST'])
def wtf():
    form = RoomRequestForm()

    if request.method == 'POST':
        if form.cancel.data:  # if cancel button is clicked, the form.cancel.data will be True
            return redirect(url_for('index')) # go back to previous page (change to room select once that page exists)

        # TODO: export all of the data from this form into the database
        # db = get_db()
        # reservation_id = string(uuid4())
        # db.execute(
        #     '''INSERT INTO reservation 
        #     (Id, User_id, Res_Date, Beg_Time, End_Time, Purpose, Organization_Id, Attendee_Count,Coffee_YN, Soda_YN, Water_YN, 
        #     Catering_YN, Lapel_Mic, Podium_Mic, Handheld_Mic, Conf_Phone, Whiteboard_YN, Easel_YN, Special_Notes, Lobby_YN, Room_Id, RoomArrangement_Id, Approved_YN) 
        #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        #     (reservation_id, user_id, res_date, beg_time, end_time, purpose, org_id, attendees, coffee, soda, water, catering, lapel_mic, podium_mic, 
        #     handheld_mic, conf_phone, whiteboard, easel, notes, no_lobby, room_id, room_arrangement_id, approved),)


    return render_template('form.html', form=form)



@forms.route('/', methods=['GET', 'POST'])
def index():

    form = RoomRequestForm()

    if request.method =='POST':
        available_rooms = get_results(form.date.data, form.start_time.data, form.end_time.data)
        return render_template('results.html', results=available_rooms)
    
    return render_template('index.html', form=form)


def get_results(date, start_time, end_time):
    db = get_db()

    available_rooms = db.execute('''SELECT * FROM room WHERE Id NOT IN 
                                (SELECT Room_Id FROM reservation WHERE Res_Date = ? AND Beg_Time <= ? AND End_Time >= ?)''', (date, end_time, start_time)).fetchall()
    
    for room in available_rooms:
        print(room['Id'], room['Name'], room['Picture_Name'], room['Capacity'])
    return available_rooms
    

    

