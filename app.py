from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import pandas as pd
from classesAndFunctions import *
import random 

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
                cur.execute("UPDATE employee SET is_terminated=1, terminated_reason=?, terminated_date=?, employee_status=? WHERE employee_id=?;", (reason, termDate, status, employeeID))
            con.commit()
            print("Employee terminated.")
        except:
            con.rollback()
            print("Something went wrong.")
        finally:
            return redirect("/terminations")
            con.close()

    # Display table of terminations
    con = sql.connect("data/hr.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT employee_name, position, department, employee_status, terminated_date, terminated_reason FROM employee WHERE is_terminated = 1 ORDER BY terminated_date DESC LIMIT 10;")
    rows = cur.fetchall()
    return render_template("terminations.html", rows = rows)

@app.route('/newHires', methods = ['POST', 'GET'])
def hires():

    # Form for adding new employees
    if request.method == 'POST':
        try:
            employeeName = request.form['employeeName']
            employeeSalary = request.form['employeeSalary']
            position = request.form['position']
            state = request.form['state']
            zipCode = request.form['zipCode']
            dob = request.form['dob']
            gender = request.form['gender']
            maritalStatus = request.form['maritalStatus']
            citizenshipStatus = request.form['citizenshipStatus']
            hispanic = request.form['hispanic']
            ethnicity = request.form['ethnicity']
            hireDate = request.form['hireDate']
            department = request.form['department']
            recruited = request.form['recruited']

            newEmployee = NewHire(employeeName, employeeSalary, position, state, zipCode, dob, gender, maritalStatus, citizenshipStatus, hispanic, ethnicity, hireDate, department, recruited)

            employee_id = random.randint(10312,99999)

            with sql.connect("data/hr.sqlite") as con:
                cur = con.cursor()
                # cur.execute("INSERT INTO employee (employee_name, employee_id) VALUES (?, ?);",(newEmployee.employeeName, newEmployee.employee_id))
                cur.execute("INSERT INTO employee VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (\
                        employee_id, newEmployee.employeeName, newEmployee.is_married(), newEmployee.marital_status_id(), newEmployee.employee_status_id(), newEmployee.department_id(), newEmployee.perf_score_id(), newEmployee.is_diversity_job_fair(), \
                        newEmployee.employeeSalary, newEmployee.is_active(), newEmployee.is_terminated(), newEmployee.position_id(), newEmployee.position, newEmployee.state, newEmployee.zipCode, newEmployee.dob, newEmployee.gender_id(), newEmployee.gender, \
                        newEmployee.is_underrep_gender(), newEmployee.maritalStatus, newEmployee.is_citizen(), newEmployee.citizenshipStatus, newEmployee.is_hispanic_latino(), newEmployee.ethnicity, newEmployee.is_underrep_race_eth(), newEmployee.hireDate, \
                        newEmployee.terminated_date(), newEmployee.terminated_reason(), newEmployee.employee_status(), newEmployee.department, newEmployee.recruited, None, None, None, 0, None, 0, 0))
            con.commit()
            print("Employee created.")
        except:
            con.rollback()
            print("Bugs bugs bugs")
        finally:
            return redirect("/newHires")
            con.close()
    
    # Create connection to database
    con = sql.connect("data/hr.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()

    # Populate positions input
    cur.execute("SELECT DISTINCT position FROM employee ORDER BY 1 ASC")
    positions = cur.fetchall()

    # Display table of most recent hires
    cur.execute("SELECT employee_name, employee_id, position, department, hired_date, source_recruiting FROM employee ORDER BY hired_date DESC LIMIT 10;")
    rows = cur.fetchall()

    return render_template('newHires.html', positions = positions, rows = rows)

@app.route('/mlModel')
def learning():
    # description of model and display code?
    # graph of data 
    # algorithm from scikitlearn
    return render_template('mlModel.html')
