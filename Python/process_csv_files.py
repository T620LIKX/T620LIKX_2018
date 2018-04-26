import helper_functions


#----------- SETTINGS - MODIFY TO FIT YOUR SETUP ------------------

data_folder = ''

write_sql_insert_statements_to_file = False
insert_directly_into_database = True

database_location = 'localhost'
database_name = 'likanx'
database_username = 'postgres'
database_password = 'postgres'

#----------- Open files and database connections as needed --------------------------

if insert_directly_into_database:
    cursor, conn = helper_functions.connect_to_database(database_location, database_name, database_username, database_password)

nem_data = helper_functions.get_data(data_folder+'studentenrollment.csv')
course_data = helper_functions.get_data(data_folder+'courses.csv')
room_data = helper_functions.get_data(data_folder+'rooms.csv')
booking_data = helper_functions.get_data(data_folder+'bookings.csv')


#----------- Process the departments --------------------------

departments = set()
for i in nem_data:
    departments.add(i['Student_Department'])
departments = list(departments)
departments.sort()

dep = {}
for i in range(len(departments)):
    dep[departments[i]] = {'id': i+1, 'name': departments[i]}


#----------- Process the students --------------------------

nemendur = set()
for i in nem_data:
    nemendur.add((i['Student_Id'], i['Student_Department']))
nemendur = list(nemendur)
nemendur.sort()

nem = {}
for i in range(len(nemendur)):
    nem[nemendur[i]] = {'id': i+1, 'student_id': nemendur[i][0], 'department_id': dep[nemendur[i][1]]['id']}


#----------- Process the rooms --------------------------

rooms_list = list()
for i in room_data:
    rooms_list.append((i['Room'], i['Description'], i['Seats']))
rooms_list.sort()

rooms = {}
for i in range(len(rooms_list)):
    rooms[rooms_list[i][0]] = {'id': i+1, 'room': rooms_list[i][0], 'description': rooms_list[i][1], 'seats': int(rooms_list[i][2]), 'exam_seats': int(rooms_list[i][2])//2 }


#----------- Process the courses --------------------------

courses = {}
counter = 1
for i in course_data:
    if i['Course_Department'] in dep.keys():
        department_id = dep[i['Course_Department']]['id']
        course_start = helper_functions.get_date_v2(i['Course_Starts'])
        course_ends = helper_functions.get_date_v2(i['Course_Ends'])

        semester_type = helper_functions.get_semester_type(course_start, course_ends)

        courses[i['Course_Id']] = {'id': counter, 'course_code': i['Course_Code'], 'course_id': i['Course_Id'], 'course_name': i['Course_Name'], 'semester': i['Semester'], 'semester_type': semester_type, 'department': i['Course_Department'], 'department_id': department_id, 'start': course_start, 'end': course_ends, 'lectures_per_week': 0, 'final_exam': False, 'exam_length': 180, 'computer_exam': False, 'problem_solving_lesson': False}
        counter = counter + 1

#----------- Process the enrollment --------------------------

enrollment = set()
for i in nem_data:
    if (i['Student_Id'], i['Student_Department']) in nem.keys() and i['Course_Id'] in courses.keys():
        student_id = nem[ (i['Student_Id'], i['Student_Department']) ]['id']
        course_id = courses[i['Course_Id']]['id']
        enrollment.add( ( student_id, course_id ))
enrollment = list(enrollment)
enrollment.sort()


#----------- Process the bookings --------------------------

for i in booking_data:
    if i['sis_Course_Id'] in courses.keys():
        if i['BookingType'] == 'Fyrirlestrar' and i['GroupName'] == '':
            semester_type = courses[i['sis_Course_Id']]['semester_type']
            courses[i['sis_Course_Id']]['lectures_per_week'] = helper_functions.calculate_lectures_per_week(semester_type, int(i['Count']))
        elif i['BookingType'] == 'Lokapróf':
            courses[i['sis_Course_Id']]['final_exam'] = True
        elif i['BookingType'] == 'Dæmatímar':
            courses[i['sis_Course_Id']]['problem_solving_lesson'] = True


#------------ Prepare the SQL insert statements --------------------------

departments_insert = "insert into departments (id, department_name) values({},'{}');"
nemendur_insert = "insert into students(id, student_no, department_id) values({},'{}',{});"
rooms_insert = "insert into rooms(id, name, seats, description, exam_seats) values({},'{}',{},'{}',{});"
courses_insert = "insert into courses(id, course_code, course_id, course_name, department_id, semester, lectures_per_week, startdate, enddate, semester_type, final_exam, exam_length, computer_exam, problem_solving_lesson) values({},'{}','{}','{}',{}, {}, {}, '{}', '{}', {}, {},{},{}, {});"
enrollment_insert = "insert into enrollment (student_id, course_id) values({},{});"


#----------------- Writing SQL insert statements to file -------------------
if write_sql_insert_statements_to_file:
    f = open('insert_statements.sql', 'w')

    for k,v in dep.items():
        f.write(departments_insert.format(v['id'], v['name']))
        f.write('\n')

    for k,v in nem.items():
        f.write(nemendur_insert.format(v['id'], v['student_id'], v['department_id']))
        f.write('\n')

    for k,v in rooms.items():
        f.write(rooms_insert.format(v['id'], v['room'], v['seats'], v['description'], v['exam_seats']))
        f.write('\n')

    for k,v in courses.items():
        f.write(courses_insert.format(v['id'], v['course_code'], v['course_id'], v['course_name'], v['department_id'], v['semester'], v['lectures_per_week'], v['start'], v['end'], v['semester_type'], v['final_exam'], v['exam_length'], v['computer_exam'], v['problem_solving_lesson']))
        f.write('\n')

    for e in enrollment:
        f.write(enrollment_insert.format(e[0], e[1]))
        f.write('\n')

    f.close()

#----------------- Insert directly into the database -------------------

if insert_directly_into_database:
    for k,v in dep.items():
        cursor.execute(departments_insert.format(v['id'], v['name']))

    for k,v in nem.items():
        cursor.execute(nemendur_insert.format(v['id'], v['student_id'], v['department_id']))

    for k,v in rooms.items():
        cursor.execute(rooms_insert.format(v['id'], v['room'], v['seats'], v['description'], v['exam_seats']))

    for k,v in courses.items():
        cursor.execute(courses_insert.format(v['id'], v['course_code'], v['course_id'], v['course_name'], v['department_id'], v['semester'], v['lectures_per_week'], v['start'], v['end'], v['semester_type'], v['final_exam'], v['exam_length'], v['computer_exam'], v['problem_solving_lesson']))

    for e in enrollment:
        cursor.execute(enrollment_insert.format(e[0], e[1]))

    conn.commit()

    cursor.close()
    conn.close()


