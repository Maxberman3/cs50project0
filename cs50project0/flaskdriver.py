from flask import Flask,render_template
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

engine = create_engine(os.getenv("postgres://bcdopqkuuoevky:509345ac532d766ae2c8d8\
09d619bbed3cb2360b468d37cdad59c81793feb837@ec2-23-23-242-163.compute-1.amazonaws.com:5432/dcc19vkphh1oms"))
db = scoped_session(sessionmaker(bind=engine))

app=Flask(__name__)

@app.route("/")
def mainpage():
    return render_template("pag1.html");