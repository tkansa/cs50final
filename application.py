from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_jsglue import JSGlue
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from random import randint
from tempfile import mkdtemp

import datetime

from articleModel import ArticleModel
from helpers import *

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///pravina.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        # get the user's preferences
        userName = login.username
        rows = db.execute("SELECT * FROM preferences WHERE user_name=:user_name", user_name=userName)
        preferences = rows[0]

        for row in rows:
            africa = row.get('africa')
            americas = row.get('americas')
            asiaPacific = row.get('asia_pacific')
            europe = row.get('europe')
            middleEast = row.get('middle_east')
            travel = row.get('travel')

        # create a list to contain the results
        results = list()

        # see if africa is selected, if so, get the articles
        if(africa == 1):
            africaResults = lookup("Africa")
        else:
            africaResults = list()

        # see if americas is selected, if so, get the articles
        if(americas == 1):
            americasResults = lookup("Americas")
        else:
            americasResults = list()

        # see if asia pacific is selected, if so, get the articles
        if(asiaPacific == 1):
            asiaPacificResults = lookup("AsiaPacific")
        else:
            asiaPacificResults = list()

        # see if europe is selected, if so, get the articles
        if(europe == 1):
            europeResults = lookup("Europe")
        else:
            europeResults = list()

        # see if middle east is selected, if so, get the articles
        if(middleEast == 1):
            middleEastResults = lookup("MiddleEast")
        else:
            middleEastResults = list()

        # see if travel is selected, if so, get the articles
        if(travel == 1):
            travelResults = lookup("Travel")
        else:
            travelResults = list()

        # append all of the results together
        for result in africaResults:
            results.append(result)

        for result in americasResults:
            results.append(result)

        for result in asiaPacificResults:
            results.append(result)

        for result in europeResults:
            results.append(result)

        for result in middleEastResults:
            results.append(result)

        for result in travelResults:
            results.append(result)

        # the number of articles returned
        num = len(results)

        # get a random number for picking the article to display
        articleIndex = randint(0, num-1)

        result = results[articleIndex]

        currentDate = datetime.date.today()

        # insert the article into the database
        db.execute("INSERT INTO articles (user_id, title, link, description, date) VALUES (:user_id, :title, :link, :description, CURRENT_TIMESTAMP)", user_id=session["user_id"], title=result['title'], link=result['link'], description=result['description'])

        data = [{"title": result['title'], "link": result['link'], "description": result['description'], "date": currentDate.strftime("%Y-%m-%d")}]

        return jsonify(data)

    # get the user's settings
    userName = login.username
    rows = db.execute("SELECT * FROM preferences WHERE user_name=:user_name", user_name=userName)

    preferences = rows[0]

    model = ArticleModel("", "", "", "", preferences['africa'], preferences['americas'], preferences['asia_pacific'], preferences['europe'], preferences['middle_east'], preferences['travel'])

    return render_template("index.html", data = model)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        login.username = request.form.get("username")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return render_template("apology.html", data = "Sorry username or password is incorrect. Please click login and try again.")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username doesn't already exist
        if len(rows) != 0:
            return render_template("apology.html", data = "This username is already taken. Please click register and try again.")

        # ensure password resubmission matches password
        if request.form.get("password") != request.form.get("password-confirmation"):
            return render_template("apology.html", data = "Password resubmission must match. Please click register and try again.")

        # insert the registrant's username and hashed password into the database
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form["username"], hash=pwd_context.hash(request.form["password"]))


        # insert a row into preference table for registrant's preferences
        db.execute("INSERT INTO preferences (user_name, africa, americas, asia_pacific, europe, middle_east, travel) values (:user_name, 0, 0, 0, 0, 0, 0)", user_name=request.form["username"])

        # redirect user to home page
        return redirect(url_for("login"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/update")
@login_required
def update():

    cat = request.args.get("category")
    chk = request.args.get("chk")

    if(cat == "0"):
        category = "africa"
    if(cat == "1"):
        category = "americas"
    if(cat == "2"):
        category = "asia_pacific"
    if(cat == "3"):
        category = "europe"
    if(cat == "4"):
        category = "middle_east"
    if(cat == "5"):
        category = "travel"

    userName = login.username

    db.execute("UPDATE preferences SET " + category + "=" + chk + " WHERE user_name=:user_name", user_name=userName )

    return ""