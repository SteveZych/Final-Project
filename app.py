from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import pandas as pd
import numpy as np
import tensorflow
from classesAndFunctions import *
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from numpy.random import seed
seed(1)

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
    rows = tableData("SELECT employee_name, position, department, employee_status, terminated_date, terminated_reason FROM employee WHERE is_terminated = 1 ORDER BY terminated_date DESC LIMIT 10;")
    
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
    
    # Populate positions input
    positions = tableData("SELECT DISTINCT position FROM employee ORDER BY 1 ASC")
    
    # Display table of most recent hires
    rows = tableData("SELECT employee_name, employee_id, position, department, hired_date, source_recruiting FROM employee ORDER BY hired_date DESC LIMIT 10;")

    return render_template('newHires.html', positions = positions, rows = rows)

@app.route('/performance', methods = ['POST', 'GET'])
def performance():
    # Form for editing existing employees for performance
    if request.method == 'POST':
        try:
            employeeID = request.form['employeeID']
            performance = request.form['performance']
            engagement = request.form['engagement']
            satisfaction = request.form['satisfaction']
            projects = request.form['projects']
            review = request.form['review']

            if performance == "Exceeds":
                perf_score_id = 4
            elif performance == "Fully Meets":
                perf_score_id = 3
            elif performance == "Needs Improvement":
                perf_score_id = 2
            else:
                perf_score_id = 1

            with sql.connect("data/hr.sqlite") as con:
                cur = con.cursor()
                cur.execute("UPDATE employee SET perf_score_id=?, perf_score=?, survey_engagement_score=?, survey_emp_satisfaction_score=?, count_special_projects=?, last_perf_review_date=? WHERE employee_id=?;", (perf_score_id, performance, engagement, satisfaction, projects, review, employeeID))
            con.commit()
            print("Performance updated.")
        except:
            con.rollback()
            print("Something went wrong.")
        finally:
            return redirect("/performance")
            con.close()

    # Display table of employees who have performance scores that need improvement or are doing improvement plans
    rows = tableData("SELECT employee_name, position, department, perf_score, last_perf_review_date FROM employee WHERE perf_score IN ('Needs Improvement' , 'PIP') ORDER BY last_perf_review_date DESC;")
    
    return render_template('performance.html', rows = rows)

@app.route('/tardy', methods = ['POST', 'GET'])
def tardy():
     # Form for editing existing employees for absence and tardiness
    if request.method == 'POST':
        try:
            employeeID = request.form['employeeID']
            absent = request.form['absent']
            late = request.form['late']

            with sql.connect("data/hr.sqlite") as con:
                cur = con.cursor()
                if absent == 1:
                    absences = cur.execute("SELECT count_absences WHERE employee_id=?;",(employeeID))
                    absences += 1
                    cur.execute("UPDATE employee SET count_absences=?, count_days_late_past_30_days=? WHERE employee_id=?;", (absences, late, employeeID))
                else:
                    cur.execute("UPDATE employee SET count_days_late_past_30_days=? WHERE employee_id=?;", (late, employeeID))
            con.commit()
            print("Absence updated.")
        except:
            con.rollback()
            print("Something went wrong.")
        finally:
            return redirect("/tardy")
            con.close()

    # Display table of most absent employees
    rows = tableData("SELECT employee_name, position, department, count_absences, count_days_late_past_30_days FROM employee ORDER BY count_absences DESC;")
    
    return render_template('tardy.html', rows = rows)

@app.route('/mlModel')
def learning():

    con = sql.connect("data/hr.sqlite")
    # con.row_factory = sql.Row
    # cur = con.cursor()
    employee = pd.read_sql_query("select is_married, is_diversity_job_fair, employee_salary, is_active, is_terminated, is_underrep_gender, is_citizen, gender_id, is_hispanic_latino, is_underrep_race_eth, survey_engagement_score, survey_emp_satisfaction_score, count_special_projects, count_days_late_past_30_days, count_absences, employee_status from employee", con)

    # dataset = cur.fetchall()
    con.close()

    X = employee.drop("employee_status", axis=1)
    y = employee["employee_status"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    X_scaler = MinMaxScaler().fit(X_train)
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)

    # Step 1: Label-encode data set
    label_encoder = LabelEncoder()
    label_encoder.fit(y_train)
    encoded_y_train = label_encoder.transform(y_train)
    encoded_y_test = label_encoder.transform(y_test)

    # Step 2: Convert encoded labels to one-hot-encoding
    y_train_categorical = to_categorical(encoded_y_train)
    y_test_categorical = to_categorical(encoded_y_test) 

    # Create model and add layers
    model = Sequential()
    model.add(Dense(units=100, activation='relu', input_dim=15))
    model.add(Dense(units=100, activation='relu'))
    model.add(Dense(units=3, activation='softmax'))

    # Compile and fit the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(
        X_train_scaled,
        y_train_categorical,
        epochs=20,
        shuffle=True,
        verbose=2
    )

    model_loss, model_accuracy = model.evaluate(X_test_scaled, y_test_categorical, verbose=2)
    loss = str(round(model_loss, 3))
    accuracy = str(round(model_accuracy, 3))

    predict_x = model.predict(X_test) 
    classes_x = np.argmax(predict_x,axis=1)
    prediction_list = list(y_test[:200])

    active_predictions = prediction_list.count('Active')
    voluntary_predictions = prediction_list.count('Voluntarily Terminated')
    cause_predictions = prediction_list.count('Terminated for Cause')
    print(active_predictions, voluntary_predictions, cause_predictions)

    active_percent = round((active_predictions / (active_predictions+voluntary_predictions+cause_predictions)),3)
    voluntary_percent = round((voluntary_predictions / (active_predictions+voluntary_predictions+cause_predictions)),3)
    cause_percent = round((cause_predictions / (active_predictions+voluntary_predictions+cause_predictions)),3)


    return render_template(
        'mlModel.html', 
        model_loss=loss, 
        model_accuracy=accuracy, 
        active_predictions=active_predictions, 
        voluntary_predictions=voluntary_predictions, 
        cause_predictions=cause_predictions, 
        active_percent=active_percent,
        voluntary_percent=voluntary_percent,
        cause_percent=cause_percent
        )
