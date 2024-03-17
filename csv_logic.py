import csv
import os
from io import StringIO

def write_csv(file, filename):
    file_path = os.path.join('csv_files', filename)
    file.save(file_path)
    return file_path

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        csv_data = csv.reader(f)
        return list(csv_data)