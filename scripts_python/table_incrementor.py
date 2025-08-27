from faker import Faker
from datetime import date, timedelta
import random
import json
import os

fake = Faker()

script_dir = os.path.dirname(os.path.abspath(__file__))
json_modules_path = os.path.join(script_dir, 'list_of_modules.json')

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
            dob = random_date(min_age, max_age)
            login = fake.word() + str(random.randint(10, 100))

            sql += f"INSERT INTO people (first_name, last_name, date_of_birth, present_role, login) VALUES ('{first_name}', '{last_name}', '{dob}', {role_id}, '{login}');\n"

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
        sql += f"INSERT INTO role_appointments (role, person, date_appointed, date_started) VALUES (1, {i}, '{date_appointed}', '{date_appointed}');\n"
    
    sql += 'COMMIT;\n'
    return sql

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
    with open(json_modules_path, 'r') as file:
        modules = json.load(file)

    sql = 'BEGIN;\n'
    for subject, module_list in modules.items():
        for module in module_list:
            sql += f"INSERT INTO modules (name, subject) SELECT '{module}', id FROM subjects where name='{subject}';\n"
    sql += 'COMMIT;\n'
    return sql

def populate_half_term_module_table(num_years=4):
    """
    Populates the half_term_module table by distributing modules for each subject across the year.
    """
    with open(json_modules_path, 'r') as file:
        modules = json.load(file)

    sql = 'BEGIN;\n'
    for year in range(1, num_years + 1):
        for subject, module_list in modules.items():
            num_modules = len(module_list)
            current_ht_id = (year - 1) * 6 + 1
            if num_modules == 6:
                for index, module_name in enumerate(module_list, start=1):
                    sql += f"INSERT INTO half_term_module (half_term, module) VALUES ((SELECT id FROM half_term WHERE number={index} and year={year}), (SELECT id FROM modules WHERE name='{module_name}'));\n"
            elif num_modules < 6:
                current_ht_number = 1
                span = 6 // num_modules
                remainder = 6 % num_modules
                ht_per_module = [span +1 if i < remainder else span for i in range(num_modules)]
                for index, module_name in enumerate(module_list):
                    for _ in range(ht_per_module[index]):
                        sql += f"INSERT INTO half_term_module (half_term, module) VALUES ((SELECT id FROM half_term WHERE number={current_ht_number} and year={year}), (SELECT id FROM modules WHERE name='{module_name}'));\n"
                        current_ht_number += 1
            else:
                span = num_modules // 6
                remainder = num_modules % 6
                module_distribution = [span +1 if i < remainder else span for i in range(6)]
                module_iter = iter(module_list)
                for index, count in enumerate(module_distribution):
                    for _ in range(count):
                        module_name = next(module_iter)
                        sql += f"INSERT INTO half_term_module (half_term, module) VALUES ((SELECT id FROM half_term WHERE number={index+1} and year={year}), (SELECT id FROM modules WHERE name='{module_name}'));\n"
    sql += 'COMMIT;\n'
    return sql

def populate_lessons_table():
    """
    Populates the lessons table with 117 lessons for each subject devided within modules.
    """
    with open(json_modules_path, "r") as file:
        modules = json.load(file)
    lessons_num = 1
    module_id_start = 1

    sql = 'BEGIN;\n'
    for subject, module_list in modules.items():
        num_modules = len(module_list)
        module_range = list(range(module_id_start, module_id_start + num_modules))
        module_id_start += num_modules
        span = 117 // num_modules
        remainder = 117 % num_modules
        lessons_per_module = [span] * num_modules
        for i in range(remainder):
            lessons_per_module[-(i+1)] += 1
        for index, count in enumerate(lessons_per_module):
            for _ in range(count):
                topic = f"{subject} - Lesson {lessons_num}"
                sql += f"INSERT INTO lessons (number, topic, module) VALUES ({lessons_num}, '{topic}', {module_range[index]});\n"
                lessons_num += 1
        lessons_num = 1  # Reset for the next subject
    sql += 'COMMIT;\n'
    return sql

def populate_assignments_table():
    """
    Populates the assignments table with an assigment for each lesson.
    """
    with open(json_modules_path, "r") as file:
        modules = json.load(file)
    lesson_list_global = []
    task_list = [
        "Learn the theory",
        "Complete online exercises",
        "Practice online",
        "Solve the worksheet",
        "Review the lecture notes"
    ]
    excluded_subjects = ["Physical Education", "Music", "Drama"]

    duplicates_info = [
        ["Mathematics", 47, date(2022, 12, 12)],
        ["Physics", 45, date(2023, 1, 31)],
        ["Chemistry", 57, date(2022, 12, 12)],
        ["Biology", 38, date(2023, 1, 11)],
        ["Science", 40, date(2023, 1, 21)],
        ["Computer Science", 59, date(2023, 1, 25)],
        ["History", 49, date(2023, 4, 21)],
        ["Geography", 60, date(2023, 3, 26)],
        ["Literature", 61, date(2023, 6, 3)],
        ["English", 39, date(2023, 3, 15)],
        ["French", 44, date(2023, 5, 13)],
        ["Spanish", 42, date(2023, 5, 28)],
        ["Latin", 55, date(2023, 6, 9)],
        ["Art", 41, date(2023, 2, 19)],
        ["Economics", 62, date(2023, 6, 16)],
        ["Philosophy", 48, date(2023, 3, 14)],
        ["Political Science", 52, date(2023, 6, 19)],
        ["Sociology", 54, date(2023, 7, 3)],
        ["Environmental Science", 51, date(2023, 5, 1)],
        ["Design & Technology", 46, date(2023, 7, 6)],
    ]

    def generate_study_days(half_terms):
        study_days = {}
        for year_num, ht_num, start, end in half_terms:
            current = start
            while current <= end:
                if current.weekday() < 5:
                    study_days.setdefault(year_num, []).append(current)
                current += timedelta(days=1)
        return study_days
    
    study_days = generate_study_days(half_terms)
    subject_patterns = {
        1: [0, 1, 3],  # Mon, Tue, Thu
        2: [1, 2, 4],  # Tue, Wed, Fri
        3: [0, 2, 3],  # Mon, Wed, Thu
        4: [1, 3, 4],  # Tue, Thu, Fri
        5: [0, 2, 4],  # Mon, Wed, Fri
    }
    
    sql = 'BEGIN;\n'
    for year, study_days_list in study_days.items():
        for index, subject in enumerate(modules.keys(), start=1):
            if subject in excluded_subjects:
                continue
            pattern_number = (index - 1) % 5 + 1
            pattern_days = subject_patterns[pattern_number]
            subject_study_days = [day for day in study_days_list if day.weekday() in pattern_days]
            for lesson_num, set_when in enumerate(subject_study_days[:117], start=1):
                lesson = {
                    "topic": f"{subject} - Lesson {lesson_num}",
                    "subject_name": subject,
                    "name": f"Assignment for Lesson #{lesson_num} in {subject}",
                    "task": random.choice(task_list),
                    "due_date": set_when + timedelta(days=random.randint(3, 15)),
                    "set_when": set_when
                }
                lesson_list_global.append(lesson)
            
    for lesson in lesson_list_global[:]:
        if lesson["subject_name"] in ["German", "Psychology", "Religious Studies"]:
            lesson["set_by"] = [25, 33, 37][["German", "Psychology", "Religious Studies"].index(lesson["subject_name"])]
        if lesson["subject_name"] == "Political Science":
            lesson["set_by"] = 34 if lesson["set_when"] < date(2022, 11, 13) else 58
        if lesson["subject_name"] == "Business Studies":
            lesson["set_by"] = 2 if lesson["set_when"] < date(2023, 3, 5) else 53
        if lesson["subject_name"] == "Civics":
            lesson["set_by"] = 34 if lesson["set_when"] < date(2022, 10, 27) else 50
        if lesson["subject_name"] in ["Mathematics", "Physics", "Chemistry", "Biology", "Science", "Computer Science", "History", "Geography", "Literature", "English", "French", "Spanish", "Latin", "Art", "Economics", "Philosophy", "Sociology", "Environmental Science", "Design & Technology"]:
            lesson["set_by"] = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 30, 31, 34, 35, 32][["Mathematics", "Physics", "Chemistry", "Biology", "Science", "Computer Science", "History", "Geography", "Literature", "English", "French", "Spanish", "Latin", "Art", "Economics", "Philosophy", "Sociology", "Environmental Science", "Design & Technology"].index(lesson["subject_name"])]
        for subject, new_id, start_date in duplicates_info:
            if lesson["subject_name"] == subject and lesson["set_when"] > start_date:
                duplicated_lesson = lesson.copy()
                duplicated_lesson["set_by"] = new_id
                lesson_list_global.append(duplicated_lesson)
    for lesson in lesson_list_global:
        sql += f"INSERT INTO assignments (lesson, name, task, due_date, set_by, set_when) SELECT id, '{lesson['name']}', '{lesson['task']}', '{lesson['due_date']}', {lesson['set_by']}, '{lesson['set_when']}' FROM lessons WHERE topic = '{lesson['topic']}';\n"
            
    sql += 'COMMIT;\n'
    return sql