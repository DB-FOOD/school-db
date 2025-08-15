from faker import Faker
from datetime import datetime
import os
from table_incrementor import populate_roles_table

fake = Faker()

output_dir = os.path.join(os.path.dirname(__file__), '..', 'seeds')
os.makedirs(output_dir, exist_ok=True)

existing_files = os.listdir(output_dir)
seed_numbers = [
    int(f.split('_')[1].split('.')[0])
    for f in existing_files if f.startswith('seed_') and f.endswith('.sql')
]
next_number = max(seed_numbers, default=0) + 1

file_name = f'seed_{next_number}.sql'
file_path = os.path.join(output_dir, file_name)

roles = ['student', 'teacher', 'principal', 'admin_staff']
sql_content = populate_roles_table(roles)

with open(file_path, "w") as f:
    f.write(sql_content)