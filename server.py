import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

from numpy import empty


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
    
def updateCompetition(number_places, index):
    with open('competitions.json') as f:
        data = json.load(f)
        data['competitions'][index]['numberOfPlaces'] = number_places
        json.dump(data, open('competitions.json', 'w'), indent=4)

def updateClub(points, index):
    with open('clubs.json') as f:
        data = json.load(f)
        data['clubs'][index]['points'] = points
        json.dump(data, open('clubs.json', 'w'), indent=4)

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

def now_date_str():
    now_date = datetime.now()
    now_str = now_date.strftime("%Y/%m/%d, %H:%M:%S")
    return now_str

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    now = now_date_str()
    if request.method == 'POST':
        club = [club for club in clubs if club['email'] == request.form['email']]
        if len(club) == 1:
            club = club[0]
            return render_template('welcome.html',club=club,competitions=competitions, now=now)
        else:
            flash("Email not found")
            return redirect(url_for("index"))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        now = now_date_str()
        if foundCompetition['date'] > now:
            return render_template('booking.html',club=foundClub,competition=foundCompetition, now=now)
        else:
            flash("impossible to book a past competition")
            return render_template('welcome.html', club=foundClub, competitions=competitions, now=now)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, now=now)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    now = now_date_str()
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = request.form['places']
    print("TEST", placesRequired)
    club_points = int(club['points'])
    if placesRequired == '':
        flash("Invalid value")
        return render_template('welcome.html', club=club, competitions=competitions, now=now)
    else:
        placesRequired = int(request.form['places'])
        if int(competition['numberOfPlaces']) >= placesRequired:
            if placesRequired <= 12:
                if club_points < placesRequired:
                    flash("Not enough points")
                    return render_template('welcome.html', club=club, competitions=competitions, now=now)
                else:
                    competition_places = int(competition['numberOfPlaces'])-placesRequired
                    club_points = int(club['points'])-placesRequired
                    flash('Great-booking complete!')
                    competition['numberOfPlaces'] = str(competition_places)
                    club['points'] = str(club_points)
                    # update json database
                    updateCompetition(number_places=competition['numberOfPlaces'], index=competitions.index(competition))
                    updateClub(points=club['points'], index= clubs.index(club))
                    return render_template('welcome.html', club=club, competitions=competitions, now=now)
            else: 
                flash('No more than 12 places can be booked')
                return render_template('welcome.html', club=club, competitions=competitions, now=now)
        else:
            flash('Not enough places') 
            return render_template('welcome.html', club=club, competitions=competitions, now=now)


@app.route('/pointDisplay')
def pointDisplay():
    all_clubs = clubs
    return render_template('points.html', all_clubs=all_clubs)
    


@app.route('/logout')
def logout():
    return redirect(url_for('index'))