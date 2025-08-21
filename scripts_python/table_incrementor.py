from faker import Faker
from datetime import date, timedelta
import random
import json

fake = Faker()

def populate_roles_table(roles):
    """
    Populates the roles table from rovided list.
    """
    sql = ''
    for role_name in roles:
        sql += f"INSERT INTO roles (role) VALUES ('{role_name}');\n"
    return sql

def populate_people_table(roles):
    """
    Populates the people table with random data.
    """
    def random_date(min_date, max_date):
        today = date.today()
        start_date = today - timedelta(days=365*max_date)
        end_date = today - timedelta(days=365*min_date)
        return fake.date_between(start_date=start_date, end_date=end_date)
    sql = 'BEGIN;\n'
    people = {
        'principal':    {'num_people': 2,   'age_range': (35, 60), 'role_id': roles.index('principal') + 1},
        'admin_staff':  {'num_people': 10,  'age_range': (22, 60),  'role_id': roles.index('admin_staff') + 1},
        'teacher':      {'num_people': 50,  'age_range': (25, 65),  'role_id': roles.index('teacher') + 1},
        'student':      {'num_people': 500, 'age_range': (12, 18),  'role_id': roles.index('student') + 1}
    }

    for role, info in people.items():
        count = info['num_people']
        min_age, max_age = info['age_range']
        role_id = info['role_id']

        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            dob = random_dob(min_age, max_age)
            login = fake.word() + str(random.randint(10, 100))

            sql += (
                f"INSERT INTO people (first_name, last_name, date_of_birth, current_role, login) "
                f"VALUES ('{first_name}', '{last_name}', '{dob}', {role_id}, '{login}' );\n"
            )

    sql += 'COMMIT;\n'
    return sql

def populate_role_appointments_table():
    """
    Populates the role_appointemnt table with random data.
    """
    opening_date = date(2022, 8, 1)
    school_start = date(2022, 9, 1)

    sql = 'BEGIN;\n'

    # First principal appointment ids 1
    sql += f"INSERT INTO role_appointments (role, person, date_appointed, date_started) VALUES (3, 1, '{opening_date}', '{opening_date}');\n"
    # a techer reapointed as a principal
    sql += f"INSERT INTO role_appointments (role, person, date_appointed, date_started) VALUES (3, 2, DATE '2023-03-01', DATE '2023-03-01');\n"
    sql += f"UPDATE role_appointments SET date_resigned=DATE '2023-03-01' WHERE person=2;\n"
    # Admin staff → ids 3–12
    for i in range(3, 12):
        date_appointed = opening_date if i < 8 else (date(2022, 8, 1) + timedelta(days=random.randint(30, 365)))
        date_started = school_start if i < 8 else (date_appointed + timedelta(days=random.randint(1,5)))
        sql += f"INSERT INTO role_appointments (role, person, date_appointed, date_started) VALUES (4, {i}, '{date_appointed}', '{date_started}');\n"

    # Teachers → ids 13–62
    for i in range(13, 63):
        date_appointed = opening_date if i < 38 else (date(2022, 8, 1) + timedelta(days=random.randint(30, 365)))
        date_started = school_start if i < 38 else (date_appointed + timedelta(days=random.randint(1, 5)))
        sql += f"INSERT INTO role_appointments (role, person, date_appointed, date_started) VALUES (2, {i}, '{date_appointed}', '{date_started}');\n"
        
    # Students → ids 63–562
    for i in range(63, 563):
        date_appointed = school_start if i < 313 else (date(2022, 9, 1) + timedelta(days=random.randint(90, 760)))
        sql += f"INSERT INTO role_appointments (role, person, date_appointed, date_stareted) VALUES (1, {i}, '{date_appointed}', '{date_appointed}');\n"

def populate_school_year_table():
    """
    Populates the school_year table with random data.
    """
    school_years = [{"name": "School Year 2022-2023", "start_date": date(2022, 9, 1), "end_date": date(2023, 7, 21)},
                    {"name": "School Year 2023-2024", "start_date": date(2023, 9, 1), "end_date": date(2024, 7, 19)},
                    {"name": "School Year 2024-2025", "start_date": date(2024, 9, 1), "end_date": date(2025, 7, 25)},
                    {"name": "School Year 2025-2026", "start_date": date(2025, 9, 1), "end_date": date(2026, 7, 24)}]
    sql = 'BEGIN;\n'

    for year in school_years:
        sql += f"INSERT INTO school_year (name, start_date, end_date) VALUES ('{year["name"]}', '{year["start_date"]}', '{year["end_date"]}');\n"
    sql += 'COMMIT;\n'
    return sql

def populate_half_term_table():
    """
    Populates the half_term table with random data.
    """
    from datetime import date

    half_terms = [
        (1, 1, date(2022, 9, 1), date(2022, 10, 21)),
        (1, 2, date(2022, 10, 31), date(2022, 12, 16)),
        (1, 3, date(2023, 1, 3), date(2023, 2, 10)),
        (1, 4, date(2023, 2, 20), date(2023, 3, 31)),
        (1, 5, date(2023, 4, 17), date(2023, 5, 26)),
        (1, 6, date(2023, 6, 5), date(2023, 7, 21)),
        (2, 1, date(2023, 9, 1), date(2023, 10, 20)),
        (2, 2, date(2023, 10, 30), date(2023, 12, 15)),
        (2, 3, date(2024, 1, 2), date(2024, 2, 9)),
        (2, 4, date(2024, 2, 19), date(2024, 3, 28)),
        (2, 5, date(2024, 4, 15), date(2024, 5, 24)),
        (2, 6, date(2024, 6, 3), date(2024, 7, 23)),
        (3, 1, date(2024, 9, 2), date(2024, 10, 25)),
        (3, 2, date(2024, 11, 4), date(2024, 12, 20)),
        (3, 3, date(2025, 1, 6), date(2025, 2, 14)),
        (3, 4, date(2025, 2, 24), date(2025, 4, 4)),
        (3, 5, date(2025, 4, 22), date(2025, 5, 23)),
        (3, 6, date(2025, 6, 2), date(2025, 7, 22)),
        (4, 1, date(2025, 9, 1), date(2025, 10, 17)),
        (4, 2, date(2025, 10, 27), date(2025, 12, 19)),
        (4, 3, date(2026, 1, 5), date(2026, 2, 13)),
        (4, 4, date(2026, 2, 23), date(2026, 4, 2)),
        (4, 5, date(2026, 4, 20), date(2026, 5, 22)),
        (4, 6, date(2026, 6, 1), date(2026, 7, 21))
    ]

    sql = 'BEGIN;\n'

    for year_id, num, start, end in half_terms:
        sql += f'INSERT INTO "half_term" (start_date, end_date, number, year) VALUES (\'{start}\', \'{end}\', {num}, {year_id});\n'

    sql += 'COMMIT;\n'
    return sql

def populate_subjects_table():
    """
    Populates the subjects table with some examle subjects.
    """
    subjects = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Science",
    "Computer Science",
    "History",
    "Geography",
    "Literature",
    "English",
    "French",
    "Spanish",
    "German",
    "Latin",
    "Art",
    "Music",
    "Physical Education",
    "Economics",
    "Philosophy",
    "Political Science",
    "Psychology",
    "Sociology",
    "Environmental Science",
    "Drama",
    "Business Studies",
    "Religious Studies",
    "Civics",
    "Design & Technology"
    ]
    sql = ''
    for subject_name in subjects:
        sql += f"INSERT INTO subjects (name) VALUES ('{subject_name}') ON CONFLICT (name) DO NOTHING;\n"
    return sql

def populate_modules_table():
    """
    Populates the modules table with data from json file.
    """
    with open('modules.json', 'r') as file:
        modules = json.load(file)

    sql = 'BEGIN;\n'
    subject_id = 1
    for subject, module_list in modules.items():
        for module in module_list:
            sql += f"INSERT INTO modules (name, subject) VALUES ('{module}', {subject_id});\n"
        subject_id += 1
    sql += 'COMMIT;\n'
    return sql

def populate_half_term_module_table(num_years=4):
    """
    Populates the half_term_module table by distributing modules for each subject across the year.
    """
    with open('modules.json', 'r') as file:
        modules = json.load(file)
    
    current_ht_id = 1
    current_mod_id = 1

    sql = 'BEGIN;\n'
    for year in range(1, num_years + 1):
        for subject, module_list in modules.items():
            num_modules = len(module_list)
            current_ht_id = (year - 1) * 6 + 1
            if num_modules == 6:
                for module_name in module_list:
                    sql += f"INSERT INTO half_term_module (half_term, module) VALUES ({current_ht_id}, {current_mod_id});\n"
                    current_ht_id +=1
                    current_mod_id += 1
            elif num_modules < 6:
                span = 6 // num_modules
                remainder = 6 % num_modules
                ht_per_module = [span +1 if i < remainder else span for i in range(num_modules)]
                for index, module_name in enumerate(module_list):
                    for _ in range(ht_per_module[index]):
                        sql += f"INSERT INTO half_term_module (half_term, module) VALUES ({current_ht_id}, {current_mod_id});\n"
                        current_ht_id += 1
                    current_mod_id += 1
            else:
                span = num_modules // 6
                remainder = num_modules % 6
                module_distribution = [span +1 if i < remainder else span for i in range(6)]
                for count in module_distribution:
                    for _ in range(count):
                        sql += f"INSERT INTO half_term_module (half_term, module) VALUES ({current_ht_id}, {current_mod_id});\n"
                        current_mod_id += 1
                    current_ht_id += 1

    sql += 'COMMIT;\n'
    return sql

