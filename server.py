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
    

def update_competitions(competitions, competition):
    competitions_json = open("competitions.json", "w")
    for data in competitions:
        if data['name'] == competition['name']:
            data['numberOfPlaces'] = str(competition['numberOfPlaces'])
    json.dump({'competitions':competitions}, competitions_json, indent=4)

        
def update_club(clubs, club):
    club_json = open("clubs.json", "w")
    for data in clubs:
        if data['name'] == club['name']:
            data['points'] = str(club['points'])
    json.dump({'clubs':clubs}, club_json, indent=4)      
        
        

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
    club = [club for club in clubs if club['email'] == request.form['email']]
    if len(club) == 1:
        club = club[0]
        return render_template('welcome.html',club=club,competitions=competitions, now=now)
    else:
        flash("Email not found")
        return redirect(url_for("index"))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    now = now_date_str()
    foundClub = [c for c in clubs if c['name'] == club]
    if len(foundClub) == 1:
        foundClub = foundClub[0]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if len(foundCompetition) == 1:
        foundCompetition = foundCompetition[0]
    if foundClub and foundCompetition:
        
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
    competition = [c for c in competitions if c['name'] == request.form['competition']]
    if len(competition) == 1:
        competition = competition[0]
    club = [c for c in clubs if c['name'] == request.form['club']]
    if len(club) == 1:
        club = club[0]
    placesRequired = request.form['places']
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
                    competitions_data = loadCompetitions()
                    clubs_data = loadClubs()
                    update_competitions(competitions_data, competition)
                    update_club(clubs_data, club)
                    
                    
                    #updateCompetition(number_places=competition['numberOfPlaces'], index=competitions.index(competition))
                    #updateClub(points=club['points'], index= clubs.index(club))
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