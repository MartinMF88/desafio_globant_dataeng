from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    id_department = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.Text)

class HiredEmployee(db.Model):
    id_employee = db.Column(db.Integer, primary_key=True)
    name_employee = db.Column(db.Text)
    hire_date = db.Column(db.TIMESTAMP(timezone=True))
    department_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)

class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    job_position = db.Column(db.Text)