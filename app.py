from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from csv_logic import write_csv, load_csv_to_db
from models import Department, HiredEmployee, Job
from database import initialize_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre@localhost/desafio_globant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
initialize_db(app)

@app.route('/upload_hired_employees_csv', methods=['POST'])
def upload_hired_employees_csv():
    try:
        hired_employees_file = request.files['hired_employees']
        file_path = write_csv(hired_employees_file, hired_employees_file.filename)
        load_csv_to_db(file_path, HiredEmployee)
        return jsonify({'message': 'Hired employees CSV uploaded and data loaded to database successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_departments_csv', methods=['POST'])
def upload_departments_csv():
    try:
        departments_file = request.files['departments']
        file_path = write_csv(departments_file, departments_file.filename)
        load_csv_to_db(file_path, Department)
        return jsonify({'message': 'Departments CSV uploaded and data loaded to database successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_jobs_csv', methods=['POST'])
def upload_jobs_csv():
    try:
        jobs_file = request.files['jobs']
        file_path = write_csv(jobs_file, jobs_file.filename)
        load_csv_to_db(file_path, Job)
        return jsonify({'message': 'Jobs CSV uploaded and data loaded to database successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)