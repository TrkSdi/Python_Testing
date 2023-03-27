import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


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
    placesRequired = int(request.form['places'])
    if int(competition['numberOfPlaces']) >= placesRequired:
        if placesRequired <= 12:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            flash('Great-booking complete!')
            # update la base de donnée json
            return render_template('welcome.html', club=club, competitions=competitions, now=now)
        else: 
            flash('No more than 12 places can be booked')
            return render_template('welcome.html', club=club, competitions=competitions, now=now)
    else:
        flash('Not enough places') 
        return render_template('welcome.html', club=club, competitions=competitions, now=now)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))