import csv
import os
from io import StringIO

def write_csv(file, filename):
    file_path = os.path.join('csv_files', filename)
    file.save(file_path)
    return os.path.abspath(file_path)

def load_csv_to_db(file_path, model):
    with open(file_path, 'r', encoding='utf-8') as f:
        csv_data = csv.reader(f)
        for row in csv_data:
            instance = model(*row)
            db.session.add(instance)
        db.session.commit()