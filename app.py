from flask import Flask,render_template,session,request
from flask_session import Session
import os
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker

app=Flask(__name__)
engine=create_engine('postgres://bcdopqkuuoevky:509345ac532d766ae2c8d809d619bbed3cb2360b468d37cdad59c81793feb837@ec2-23-23-242-163.compute-1.amazonaws.com:5432/dcc19vkphh1oms')
db=engine.connect()
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://bcdopqkuuoevky:509345ac532d766ae2c8d809d619bbed3cb2360b468d37cdad59c81793feb837@ec2-23-23-242-163.compute-1.amazonaws.com:5432/dcc19vkphh1oms'
#db=SQLAlchemy(app)

Session(app)

@app.route("/")
def mainpage():
    return render_template("pag1.html")
@app.route("/page2.html")
def boatpage():
    return render_template("page2.html")
@app.route("/page3.html")
def crewpage():
    return render_template("page3.html")
@app.route("/page4.html")
def timespage():
    return render_template("page4.html")
@app.route("/createaccount.html", methods=['GET','POST'])
def createaccountpage():
    return render_template("createaccount.html")
@app.route("/testcreation" ,methods=['GET','POST'])
def testcreation():
    username=request.form.get("username")
    password=request.form.get("passcode")
    #print('form requests were accepted', file=std.out)
    testresults=db.execute("SELECT * FROM users WHERE username= '"+username+"' AND password= '"+password +"';").fetchall()
    #print('got past fetch',file=std.out)
    if len(testresults) == 0:
        #print('got past rowcount test, success',file=std.out)
        db.execute("INSERT INTO users (username,password) VALUES ('"+username+"','"+password+"');")
        return 'success! this username has not been taken'
    else:
        #print('got past rowcount test, fail',file=std.out)
        return 'fail! this username has already been taken'
@app.route("/login.html")
def login():
    return render_template("login.html")
