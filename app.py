from flask import Flask,render_template,session,request,redirect, url_for
#from flask_session import Session
import os
import sys
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date

app=Flask(__name__)
app.secret_key=os.urandom(24)
engine=create_engine('postgres://bcdopqkuuoevky:509345ac532d766ae2c8d809d619bbed3cb2360b468d37cdad59c81793feb837@ec2-23-23-242-163.compute-1.amazonaws.com:5432/dcc19vkphh1oms')
db=engine.connect()
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://bcdopqkuuoevky:509345ac532d766ae2c8d809d619bbed3cb2360b468d37cdad59c81793feb837@ec2-23-23-242-163.compute-1.amazonaws.com:5432/dcc19vkphh1oms'
#db=SQLAlchemy(app)


@app.route("/")
def mainpage():
    if 'username' in session:
        loggedin=True
    else:
        loggedin=False
    return render_template("pag1.html", loggedin=loggedin)
@app.route("/page2.html")
def boatpage():
    return render_template("page2.html")
@app.route("/page3.html")
def crewpage():
    return render_template("page3.html")
#grabs cruises from db to populate table
@app.route("/page4.html")
def timespage():
    cruises=db.execute("SELECT * FROM cruises;").fetchall()
    return render_template("page4.html",cruises=cruises)
#renders createaccount template and posts username and password to the testcreation method/url
@app.route("/createaccount.html")
def createaccountpage():
    return render_template("createaccount.html")
#tests if the username is already in the database and informs them if it is. if not the account is created and added to the db
@app.route("/testcreation" ,methods=['POST'])
def testcreation():
    username=request.form.get("username")
    password=request.form.get("passcode")
    if len(username)<5 or len(password)<5 or len(username)>16 or len(password)>16:
        return render_template('createfail2.html')
    testresults=db.execute("SELECT * FROM users WHERE username= '"+username+"';").fetchall()
    if len(testresults) == 0:
        db.execute("INSERT INTO users (username,password) VALUES ('"+username+"','"+password+"');")
        return render_template("createsuccess.html")
    else:
        return render_template("createfail.html")
@app.route("/login.html")
def login():
    return render_template("login.html")
#tests to see if login and password are in database
@app.route("/loginsf",methods=['POST'])
def logintest():
    username=request.form.get("username")
    password=request.form.get("passcode")
    logintest=db.execute("SELECT * FROM users WHERE username= '"+username+"' AND password= '"+password+"';").fetchall()
    if len(logintest) == 0:
        return render_template('loginfail.html')
    else:
        session['username']= username
        return render_template("loggedin.html")
#signs the user out of the session
@app.route("/signout")
def signout():
    session.pop('username',None)
    return redirect(url_for('mainpage'))
#fetches the reviews from the database in order to render them on the site
@app.route("/reviews.html")
def reviews():
    empty=False
    reviewtable=db.execute("SELECT * FROM reviews;").fetchall()
    if len(reviewtable) == 0:
        empty=True
    return render_template('reviews.html', reviewtable=reviewtable, empty=empty)
#renders a form for the user to submit a review
@app.route("/reviewsubmit")
def reviewsubmit():
    cruisetable=db.execute("SELECT * FROM cruises;").fetchall()
    return render_template('reviewform.html', cruisetable=cruisetable)
#submits the review to the db and redirects to the reviews page
@app.route("/reviewenter",methods=['POST'])
def reviewenter():
    username=session['username'];
    todaysdate=str(date.today())
    contents=request.form.get("reviewcontents")
    cruiseid=request.form.get("cruise")
    if len(cruiseid)==0 or len(contents)<11 or len(contents)>3000:
        return render_template('reviewsubmitfail.html')
    contents.replace("'","")
    insrtcommand="INSERT INTO reviews (username,submission_date,contents,cruise) VALUES ('{}','{}','{}',{})".format(username,todaysdate,contents,cruiseid)
    db.execute(insrtcommand)
    return redirect(url_for('reviews'))
#renders a template to input passenger information and to choose a cruise to get tickets for. also provides links to individual cruise pages
@app.route("/ticket_signup")
def gettix():
    cruises=db.execute("SELECT id,origin,destination FROM cruises;").fetchall()
    return render_template('gettix.html',cruises=cruises)
#inputs the information to the passenger table of the db and informs the passenger their reservation is made as well as details of attendance
@app.route("/ticketsubmit", methods=['POST'])
def ticketsubmit():
    firstname=request.form.get("first_name")
    lastname=request.form.get("last_name")
    cruise=request.form.get("cruise")
    if firstname.isspace() or lastname.isspace() or cruise == None or cruise.isspace():
        return render_template('ticketfail.html')
    insrtcommand="INSERT INTO passengers (first_name,last_name,cruise) VALUES ('{}','{}',{});".format(firstname,lastname,cruise)
    db.execute(insrtcommand)
    passengername=firstname+" "+lastname
    cruiseinfo=(db.execute("SELECT origin,destination FROM cruises WHERE id={};".format(cruise)).fetchall())[0]
    return render_template('gottix.html', cruiseinfo=cruiseinfo, passengername=passengername)
@app.route("/cruises/<int:cruiseid>")
def cruisedeets(cruiseid):
    cruise=db.execute("SELECT * FROM cruises WHERE id={};".format(cruiseid)).fetchall()[0]
    passengers=db.execute("SELECT first_name,last_name FROM passengers WHERE cruise= {};".format(cruiseid)).fetchall()
    return render_template('details.html',cruise=cruise,passengers=passengers)
