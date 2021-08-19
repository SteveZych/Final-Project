import sqlite3 as sql

class NewHire():
    def __init__(self, employeeName, employeeSalary, position, state, zipCode, dob, gender, martialStatus, citizenshipStatus, hispanic, ethnicity, hireDate, department, recruited):
        self.employeeName = employeeName
        self.employeeSalary = employeeSalary
        self.position = position
        self.state = state
        self.zipCode = zipCode
        self.dob = dob
        self.gender = gender
        self.maritialStatus = martialStatus
        self.citizenshipStatus = citizenshipStatus
        self.hispanic = hispanic
        self.ethnicity = ethnicity
        self.hireDate = hireDate
        self.department = department
        self.recruited = recruited

    def employee_id():
        con = sql.connect("data/hr.sqlite")
        cur = con.cursor()
        employeeCount = cur.execute("SELECT COUNT(employee_id) FROM employee")
        return employeeCount + 1

    def is_married(self):
        if self.maritialStatus == "Married":
            cell = 1
        else:
            cell = 0
        return cell

    def maritial_status_id(self):
        if self.maritialStatus == "Married":
            cell = 1
        elif self.maritialStatus == "Divorced":
            cell = 2
        elif self.maritialStatus == "Separated":
            cell = 3
        elif self.maritialStatus == "Widowed":
            cell = 4
        else:
            cell = 0
        return cell
        
    def gender_id(self):
        if self.gender == "F":
            cell = 0
        else:
            cell = 1
        return cell

    def employee_status_id(self):
        # Needs evaluation, number 1 overlaps with multiple employment status
        pass

    def department_id(self):
        # Same as above, missing number 2
        pass

    def perf_score_id(self):
        pass

    def is_diversity_job_fair(self):
        pass
        
    def position_id(self):
        pass



def tableData(query):
    con = sql.connect("data/hr.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows
