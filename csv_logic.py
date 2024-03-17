import csv
from io import StringIO
import os
from models import db

def write_csv(file, filename):
    file_path = os.path.join('csv_files', filename)
    file.save(file_path)
    return file_path

def load_csv_to_db(file_path, model):
    data = open(file_path, 'r').read().decode('utf-8')
    csv_data = csv.reader(StringIO(data))
    for row in csv_data:
        instance = model(*row)
        db.session.add(instance)
    db.session.commit()