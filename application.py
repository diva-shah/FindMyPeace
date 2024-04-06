import os

from cs50 import SQL 
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# API_KEY
# export API_KEY=pk_3142b8f25f584f958e90790311d4dc28
# export FLASK_APP=application
# export FLASK_ENV=developement
# Configure application
app = Flask(__name__)
#global variable
USERS = {}
information = []
dup = []
shares2 = []

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///findmypeace.db")



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Make sure API key is set

# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == 'GET':
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        name = request.form.get("username")
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
        print("ID: ", session['user_id'])
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    punctuation = False
    number = False
    length = False
    characters = False
    if request.method == "POST":
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords are not the same!")

        if not request.form.get("username"):
            return apology("Missing Username")

        if not request.form.get("password"):
            return apology("Missing Password")

        if not request.form.get("confirmation"):
            return apology("You forgot to re-enter your password!")
        password = request.form.get("password")
        for x in password:
            if x == '!' or x == '?' or x == '.':
                punctuation = True
            if x.isnumeric() == True:
                number = True
            if isinstance(x, str) == True and x != '!' and x != '?' and x != '.':
                characters = True
        if len(password) >= 8:
            length = True
        check = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if (len(check) > 0):
            return apology("Username Taken")
        if length == False or number == False or punctuation == False or characters == False:
            return apology("Password has to have and can only have punctuation, characters, numbers, and has to be at leats 8 characters long")

        check2 = db.execute("SELECT hash FROM users WHERE hash = ?", generate_password_hash(request.form.get("password")))
        if (len(check2) > 0):
            return apology("Password Taken")
        db.execute("INSERT INTO users (username,hash) VALUES(?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
    else:
        return render_template("register.html")
    return redirect("/")