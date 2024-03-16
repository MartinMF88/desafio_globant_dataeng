from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
from io import StringIO
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgre:postgre@localhost/desafio_globant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir modelos de las tablas
class Department(db.Model):
    id_department = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.Text)

class HiredEmployee(db.Model):
    id_employee = db.Column(db.Integer, primary_key=True)
    name_employee = db.Column(db.Text)
    hire_date = db.Column(db.TIMESTAMP(timezone=True))
    data_1 = db.Column(db.Integer)
    data_2 = db.Column(db.Integer)

class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    job_position = db.Column(db.Text)

# Ruta para cargar los archivos CSV
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        # Obtener archivos CSV del cuerpo de la solicitud
        hired_employees_file = request.files['hired_employees']
        departments_file = request.files['departments']
        jobs_file = request.files['jobs']

        # Cargar datos CSV a la base de datos
        load_csv_to_db(hired_employees_file, departments_file, jobs_file)

        return jsonify({'message': 'CSV files uploaded and data loaded to database successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Función para cargar datos CSV a la base de datos PostgreSQL
def load_csv_to_db(hired_employees_file, departments_file, jobs_file):
    # Obtener la ruta completa a los archivos CSV
    hired_employees_path = os.path.join('csv_files', hired_employees_file.filename)
    departments_path = os.path.join('csv_files', departments_file.filename)
    jobs_path = os.path.join('csv_files', jobs_file.filename)

    # Guardar los archivos CSV en el sistema de archivos
    hired_employees_file.save(hired_employees_path)
    departments_file.save(departments_path)
    jobs_file.save(jobs_path)

    # Leer datos de archivos CSV
    departments_data = open(departments_path, 'r').read().decode('utf-8')
    jobs_data = open(jobs_path, 'r').read().decode('utf-8')
    hired_employees_data = open(hired_employees_path, 'r').read().decode('utf-8')

    # Cargar datos de departamentos
    departments_csv = csv.reader(StringIO(departments_data))
    for row in departments_csv:
        department = Department(id_department=row[0], department=row[1])
        db.session.add(department)

    # Cargar datos de trabajos
    jobs_csv = csv.reader(StringIO(jobs_data))
    for row in jobs_csv:
        job = Job(job_id=row[0], job_position=row[1])
        db.session.add(job)

    # Cargar datos de empleados contratados
    hired_employees_csv = csv.reader(StringIO(hired_employees_data))
    batch_size = 1000  # Tamaño del lote
    rows = []
    for row in hired_employees_csv:
        hired_employee = HiredEmployee(id_employee=row[0], name_employee=row[1], hire_date=row[2], data_1=row[3], data_2=row[4])
        rows.append(hired_employee)
        if len(rows) >= batch_size:
            db.session.bulk_save_objects(rows)
            db.session.commit()
            rows = []
    if rows:  # Insertar el resto de las filas que quedaron en el lote final
        db.session.bulk_save_objects(rows)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)