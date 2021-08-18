from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tables")
def tables():
    con = sql.connect("data/hr.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from employee")
    rows = cur.fetchall()
    return render_template("tables.html", rows = rows)

@app.route('/terminations', methods = ['POST', 'GET'])
def terminations():
    
    # Form for editing existing employees for termination
    if request.method == 'POST':
        try:
            employeeID = request.form['employeeID']
            reason = request.form['reason']
            termDate = request.form['termDate']
            status = request.form['status']

            with sql.connect("data/hr.sqlite") as con:
                cur = con.cursor()
                cur.execute("UPDATE employee SET is_terminated=1, terminated_reason=?, terminated_date=?, employee_status=? WHERE employee_id=?", (reason, termDate, status, employeeID))
            con.commit()
            print("Employee terminated.")
        except:
            con.rollback()
            print("Something went wrong.")
        finally:
            return redirect("/terminations")
            con.close()

    # Display table of terminations, query "SELECT * FROM employee WHERE is_terminated = "1" ORDER BY employee_id DESC LIMIT 10"
    con = sql.connect("data/hr.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM employee WHERE is_terminated = 1 ORDER BY terminated_date DESC LIMIT 10")
    rows = cur.fetchall()
    return render_template("terminations.html", rows = rows)

# @app.route('/newHires')
# def terminations():
#     # Display table of most recent hires
#     # Form for adding new employees
#     return render_template('newHires.html')

# @app.route('/mlModel')
# def learning():
#     # description of model and display code?
#     # graph of data 
#     # algorithm from scikitlearn
#     return render_template('mlModel.html')
