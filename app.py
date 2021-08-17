from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tables")  
def tables():  
    con = sql.connect("hr.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from employees")
    rows = cur.fetchall()
    return render_template("tables.html", rows = rows)

@app.route('/terminations')
def terminations():
    # Display table of terminations
    # Form for editing existing employees for termination
    return render_template('terminations.html')

@app.route('/newHires')
def terminations():
    # Display table of most recent hires
    # Form for adding new employees
    return render_template('newHires.html')

@app.route('/mlModel')
def learning():
    # description of model and display code?
    # graph of data 
    # algorithm from scikitlearn
    return render_template('mlModel.html')