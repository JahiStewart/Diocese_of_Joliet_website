from flask import Blueprint, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SubmitField
from wtforms.validators import InputRequired
from flaskr.db import get_db
from uuid import uuid4

forms = Blueprint('form', __name__)

class RoomRequestForm(FlaskForm):
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