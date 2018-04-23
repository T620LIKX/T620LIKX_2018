drop table solutions;
drop table enrollment;
drop table students;
drop table rooms;
drop table courses;
drop table departments;

#---------------------------------

create table departments(
    id integer,
    department_name varchar(256),
    primary key (id)
);

create table courses (
    id integer,
    course_code varchar(256),
    course_id varchar(256) unique,
    course_name varchar(256),
    department_id integer references departments(id),
    semester integer,
    semester_type integer,
    lectures_per_week integer,
    non_consecutive_days bool,
    final_exam boolean,
    exam_length int,
    computer_exam boolean,
    startdate date,
    enddate date,
    primary key (id)
);

create table rooms (
    id integer,
    name varchar(256) unique,
    seats integer,
    description varchar(256),
    exam_seats integer,
    primary key (id)
);

create table students (
    id integer,
    student_no varchar(256),
    department_id int references departments(id),
    primary key (id)
);

create table enrollment(
    student_id integer references students(id),
    course_id integer references courses(id),
    primary key (student_id, course_id)
);

create table solutions (
    id serial,
    solution_id integer,
    solution_type varchar(256),
    course_id integer REFERENCES courses(id),
    room_id integer REFERENCES rooms(id),
    timeslot integer,
    primary key (id)
);


