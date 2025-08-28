CREATE TABLE "people"(
    "id" bigserial NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "date_of_birth" DATE NOT NULL,
    "present_role" BIGINT NOT NULL,
    "login" VARCHAR(255) NULL
);
ALTER TABLE
    "people" ADD PRIMARY KEY("id");
CREATE TABLE roles (
    id bigserial PRIMARY KEY,
    role VARCHAR(255) NOT NULL CHECK (
        role IN ('student', 'teacher', 'principal', 'admin_staff')
    ),
    CONSTRAINT unique_role UNIQUE (role)
);
CREATE TABLE "school_year"(
    "id" bigserial NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL
);
ALTER TABLE
    "school_year" ADD PRIMARY KEY("id");
CREATE TABLE "lessons"(
    "id" bigserial NOT NULL,
    "number" INTEGER NOT NULL,
    "topic" VARCHAR(255) NOT NULL,
    "module" BIGINT NOT NULL
);
ALTER TABLE
    "lessons" ADD PRIMARY KEY("id");
CREATE TABLE "subjects"(
    "id" bigserial NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "subjects" ADD PRIMARY KEY("id");
ALTER TABLE "subjects"
    ADD CONSTRAINT unique_subjects_name UNIQUE ("name");
CREATE TABLE "half_term"(
    "id" bigserial NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "number" INTEGER NOT NULL,
    "year" BIGINT NOT NULL
);
ALTER TABLE
    "half_term" ADD PRIMARY KEY("id");
CREATE TABLE "assignments"(
    "id" bigserial NOT NULL,
    "lesson" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "task" VARCHAR(255) NOT NULL,
    "due_date" DATE NOT NULL,
    "set_by" BIGINT NOT NULL,
    "set_when" DATE NOT NULL
);
ALTER TABLE
    "assignments" ADD PRIMARY KEY("id");
CREATE TABLE "modules"(
    "id" bigserial NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "subject" BIGINT NOT NULL
);
ALTER TABLE
    "modules" ADD PRIMARY KEY("id");
CREATE TABLE "studying_track"(
    "assignment" BIGINT NOT NULL,
    "student" BIGINT NOT NULL,
    "assigned_when" DATE NOT NULL,
    "started_when" DATE,
    "completed_when" DATE,
    "grade" VARCHAR(255) CHECK
        ("grade" IN('1', '2', '3', '4', '5', 'ACCEPTED', 'REJECTED')) NULL,
        "when_graded" DATE NULL,
        "who_graded" BIGINT NULL
);
ALTER TABLE "studying_track"
  ADD PRIMARY KEY ("assignment", "student");

CREATE TABLE "half_term_module"(
    "id" bigserial NOT NULL,
    "half_term" BIGINT NOT NULL,
    "module" BIGINT NOT NULL
);
ALTER TABLE
    "half_term_module" ADD PRIMARY KEY("id");
CREATE TABLE "role_appointments"(
    "id" bigserial NOT NULL,
    "role" BIGINT NOT NULL,
    "person" BIGINT NOT NULL,
    "date_appointed" DATE NOT NULL,
    "date_started" DATE NOT NULL,
    "date_resigned" DATE NULL
);
ALTER TABLE
    "role_appointments" ADD PRIMARY KEY("id");
CREATE TABLE "classes"(
    "id" bigserial NOT NULL,
    "lesson" BIGINT NOT NULL,
    "time_started" TIMESTAMP NOT NULL,
    "time_ended" TIMESTAMP NOT NULL,
    "location" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "classes" ADD PRIMARY KEY("id");
CREATE TABLE "attendance"(
    "class" BIGINT NOT NULL,
    "person" BIGINT NOT NULL,
    "role" BIGINT NOT NULL,
    "time_arrived" TIMESTAMP NOT NULL
);
ALTER TABLE "attendance"
  ADD PRIMARY KEY ("class", "person");
ALTER TABLE
    "studying_track" ADD CONSTRAINT "studying_track_student_foreign" FOREIGN KEY("student") REFERENCES "people"("id");
ALTER TABLE
    "assignments" ADD CONSTRAINT "assignments_set_by_foreign" FOREIGN KEY("set_by") REFERENCES "people"("id");
ALTER TABLE
    "half_term_module" ADD CONSTRAINT "half_term_module_half_term_foreign" FOREIGN KEY("half_term") REFERENCES "half_term"("id");
ALTER TABLE
    "attendance" ADD CONSTRAINT "attendance_person_foreign" FOREIGN KEY("person") REFERENCES "people"("id");
ALTER TABLE
    "attendance" ADD CONSTRAINT "attendance_class_foreign" FOREIGN KEY("class") REFERENCES "classes"("id");
ALTER TABLE
    "attendance" ADD CONSTRAINT "attendance_role_foreign" FOREIGN KEY("role") REFERENCES "roles"("id");
ALTER TABLE 
    "people" ADD CONSTRAINT "people_present_role_foreign" FOREIGN KEY ("present_role") REFERENCES "roles"("id");
ALTER TABLE
    "role_appointments" ADD CONSTRAINT "role_appointments_role_foreign" FOREIGN KEY("role") REFERENCES "roles"("id");
ALTER TABLE
    "role_appointments" ADD CONSTRAINT "role_appointments_person_foreign" FOREIGN KEY("person") REFERENCES "people"("id");
ALTER TABLE
    "studying_track" ADD CONSTRAINT "studying_track_who_graded_foreign" FOREIGN KEY("who_graded") REFERENCES "people"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_module_foreign" FOREIGN KEY("module") REFERENCES "modules"("id");
ALTER TABLE
    "studying_track" ADD CONSTRAINT "studying_track_assignment_foreign" FOREIGN KEY("assignment") REFERENCES "assignments"("id");
ALTER TABLE
    "half_term" ADD CONSTRAINT "half_term_year_foreign" FOREIGN KEY("year") REFERENCES "school_year"("id");
ALTER TABLE
    "assignments" ADD CONSTRAINT "assignments_lesson_foreign" FOREIGN KEY("lesson") REFERENCES "lessons"("id");
ALTER TABLE
    "classes" ADD CONSTRAINT "classes_lesson_foreign" FOREIGN KEY("lesson") REFERENCES "lessons"("id");
ALTER TABLE
    "modules" ADD CONSTRAINT "modules_subject_foreign" FOREIGN KEY("subject") REFERENCES "subjects"("id");
ALTER TABLE
    "half_term_module" ADD CONSTRAINT "half_term_module_subject_foreign" FOREIGN KEY("module") REFERENCES "modules"("id");