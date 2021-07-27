import json
from flask import Flask, render_template, request, redirect, flash, url_for
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, clubs=clubs, competitions=competitions)
    except IndexError:
        flash("Invalid email")
        return render_template("index.html", clubs=clubs), 403


@app.route('/book/<competition>/<club>')
def book(competition, club):
    print(f'competitions {competitions}')
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    for c in competitions:
        if c['name'] == competition:
            competitionData = c
            print(f'c {c}')
    foundCompetitionDate = competitionData['date']
    print(f'foundCompetitionDate {foundCompetitionDate}')
    if datetime.strptime(str(foundCompetitionDate), "%Y-%m-%d %H:%M:%S") <= datetime.now():
        flash("booking allowed only for future competition")
        return redirect(url_for('index'), 302)
    elif foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > int(club['points']) or placesRequired < 0 or placesRequired > 12:
        flash("Max points allowed should be 12 per competition")
        return redirect(url_for('index'), 302)
    else:
        club['points'] = int(club['points']) - placesRequired
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
