import os
import table_incrementor
# from table_incrementor import populate_roles_table
# from table_incrementor import populate_people_table
# from table_incrementor import populate_role_appointments_table
# from table_incrementor import populate_subjects_table
# from table_incrementor import populate_school_year_table
# from table_incrementor import populate_half_term_table
# from table_incrementor import populate_modules_table
# from table_incrementor import populate_half_term_module_table
# from table_incrementor import populate_lessons_table
# from table_incrementor import populate_assignments_table

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
sql_content += '\n' + table_incrementor.populate_people_table(roles)
sql_content += '\n' + populate_role_appointments_table()
sql_content += '\n' + populate_school_year_table()
sql_content += '\n' + populate_half_term_table()
sql_content += '\n' + populate_subjects_table()
sql_content += '\n' + populate_modules_table()
sql_content += '\n' + populate_half_term_module_table(num_years=4)
sql_content += '\n' + populate_lessons_table()
sql_content += '\n' + populate_assignments_table()

with open(file_path, "w") as f:
    f.write(sql_content)

# in case we would like to have a separate file for each table we will need to increment next_number before each table
# next_number += 1
# file_name_subjects = f'seed_{next_number}_subjects.sql'
# file_path_subjects = os.path.join(output_dir, file_name_subjects)

# if __name__ == "__main__":
 run another 