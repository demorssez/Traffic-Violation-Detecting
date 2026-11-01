import csv
from datetime import datetime
from pathlib import Path

def append_violation(csv_path, id, plate, speed):
    new_file = not Path(csv_path).exists()
    with open(csv_path, 'a', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(['Time', 'ID', 'Plate', 'Speed_kmh'])
        writer.writerow([datetime.now().isoformat(sep = ' ', timespec = 'seconds'), id, plate, round(speed, 1)])