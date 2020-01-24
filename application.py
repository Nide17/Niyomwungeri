import os

from flask import Flask, session, redirect, render_template, request
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from datetime import datetime

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/project")
def project():
    return render_template("project.html")    

@app.route("/about")
def about():
    return render_template("about.html")    

@app.route("/contact")
def contact():
    return render_template("contact.html")   
     

@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    """subscribe"""
    
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return render_template("error.html", message="Please enter your Email")

        # Query database for email
        userCheck = db.execute("SELECT * FROM subscribers WHERE email = :email",
                          {"email":request.form.get("email")}).fetchone()

        # Check if email already exist
        if userCheck:
            return render_template("error.html", message="Email already subscribed. use a different one")

        # Insert email into DB
        dt = datetime.now()

        db.execute("INSERT INTO subscribers (email, sub_time) VALUES (:email, :sub_time)",
                            {"email":request.form.get("email"), 
                             "sub_time":dt})

        # Commit changes to database
        db.commit()

        # Redirect user to Home page
        return render_template("success.html", message="You are now subscribed.")  


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/")


@app.route("/message", methods=["GET", "POST"])
def message():
    """send a message"""
    
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure Username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="Your name is required")

        # Ensure email was submitted
        if not request.form.get("email"):
            return render_template("error.html", message="Email is required")

        # Ensure Message was submitted
        if not request.form.get("message"):
            return render_template("error.html", message="Message is required")    

        # Insert email into DB
        dt = datetime.now()

        db.execute("INSERT INTO messages (username, email, msg_content, msg_time) VALUES (:username, :email, :msg_content, :msg_time)",
                            {"username":request.form.get("username"), "email":request.form.get("email"), "msg_content":request.form.get("message"), 
                             "msg_time":dt})

        # Commit changes to database
        db.commit()

        # Redirect user to Home page
        return render_template("success.html", message="You are message is sent! Thank you.")  


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/contact")        
