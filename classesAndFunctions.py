import sqlite3 as sql

class NewHire():
    def __init__(self, employeeName, employeeSalary, position, state, zipCode, dob, gender, maritalStatus, citizenshipStatus, hispanic, ethnicity, hireDate, department, recruited):
        self.employeeName = employeeName
        self.employeeSalary = employeeSalary
        self.position = position
        self.state = state
        self.zipCode = zipCode
        self.dob = dob
        self.gender = gender
        self.maritalStatus = maritalStatus
        self.citizenshipStatus = citizenshipStatus
        self.hispanic = hispanic
        self.ethnicity = ethnicity
        self.hireDate = hireDate
        self.department = department
        self.recruited = recruited

    def is_married(self):
        if self.maritalStatus == "Married":
            cell = 1
        else:
            cell = 0
        return cell

    def maritial_status_id(self):
        if self.maritalStatus == "Married":
            cell = 1
        elif self.maritalStatus == "Divorced":
            cell = 2
        elif self.maritalStatus == "Separated":
            cell = 3
        elif self.maritalStatus == "Widowed":
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

    def employee_status():
        return "Active"

    def is_active():
        return 1

    def is_terminated():
        return 0

    def employee_status_id(self):
        return 1

    def department_id(self):
        if self.department == "Executive Office":
            cell = 1
        elif self.department == "Admin Offices":
            cell = 2
        elif self.department == "IT/IS":
            cell = 3
        elif self.department == "Software Engineering":
            cell = 4
        elif self.department == "Production":
            cell = 5
        elif self.department == "Sales":
            cell = 6
        else:
            cell = 0
        return cell

    def perf_score_id(self):
        return None

    def terminated_date(self):
        return None    

    def terminated_reason(self):
        return None

    def is_hispanic_latino(self):
        if self.hispanic == "Yes":
            cell = 1
        else:
            cell = 0
        return cell

    def is_citizen(self):
        if self.citizenshipStatus == "US Citizen":
            cell = 1
        else:
            cell = 0
        return cell

    def is_diversity_job_fair(self):
        if self.recruited == "Diversity Job Fair":
            cell = 1
        else:
            cell = 0
        return cell

    def is_underrep_gender(self):
        if self.gender == "F":
            cell = 1
        else:
            cell = 0
        return cell

    def is_underrep_race_eth(self):
        if self.ethnicity == "White":
            cell = 0
        else:
            cell = 1
        return cell
        
    def position_id(self):
        if self.position == "Accountant I":
            cell = 1
        elif self.position == "Administrative Assistant":
            cell = 2
        elif self.position == "Area Sales Manager":
            cell = 3
        elif self.position == "BI Developer":
            cell = 4
        elif self.position == "BI Director":
            cell = 5
        elif self.position == "CIO":
            cell = 6
        elif self.position == "Data Architect":
            cell = 7
        elif self.position == "Database Administrator":
            cell = 8
        elif self.position == "Data Analyst":
            cell = 9
        elif self.position == "Director of Operations":
            cell = 10
        elif self.position == "Director of Sales":
            cell = 11
        elif self.position == "IT Director":
            cell = 12
        elif self.position == "IT Manager - DB":
            cell = 13
        elif self.position == "IT Manager - Support":
            cell = 14
        elif self.position == "IT Manager - Infra":
            cell = 15
        elif self.position == "IT Support":
            cell = 16
        elif self.position == "Network Engineer":
            cell = 17
        elif self.position == "President & CEO":
            cell = 18
        elif self.position == "Production Manager":
            cell = 19
        elif self.position == "Production Technician I":
            cell = 20
        elif self.position == "Production Technician II":
            cell = 21
        elif self.position == "Sales Manager":
            cell = 22
        elif self.position == "Senior BI Developer":
            cell = 23
        elif self.position == "Software Engineer":
            cell = 24
        elif self.position == "Shared Services Manager":
            cell = 25
        elif self.position == "Software Engineering Manager":
            cell = 27
        elif self.position == "Sr. Accountant":
            cell = 28
        elif self.position == "Sr. DBA":
            cell = 29
        elif self.position == "Sr. Network Engineer":
            cell = 30
        elif self.position == "Principal Data Architect":
            cell = 31
        elif self.position == "Enterprise Architect":
            cell = 32
        else:
            cell = 0
        return cell

    # @staticmethod
    # def employee_id():
    #     con = sql.connect("data/hr.sqlite")
    #     cur = con.cursor()
    #     employeePK = cur.execute("SELECT MAX(employee_id) FROM employee")
    #     return employeePK + 1
        



# def tableData(query):
#     con = sql.connect("data/hr.sqlite")
#     con.row_factory = sql.Row
#     cur = con.cursor()
#     cur.execute(query)
#     rows = cur.fetchall()
#     return rows
