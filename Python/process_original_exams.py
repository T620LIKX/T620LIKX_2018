import helper_functions

data_folder = ''

write_sql_insert_statements_to_file = False
insert_directly_into_database = True

database_location = 'localhost'
database_name = 'likanx'
database_username = 'postgres'
database_password = 'postgres'

if insert_directly_into_database:
    cursor, conn = helper_functions.connect_to_database(database_location, database_name, database_username, database_password)

data = helper_functions.get_data(data_folder+'exams.csv')

exams = set()
for i in data:
    exams.add((i['DAGSETNING'], i['HEFST'], i['ENDAR'], i['NAMSGREIN'], i['HEITI'], i['STOFA'], i['NAFN STOFU'], i['BYGGING']))
exams = list(exams)
exams.sort()


exam = {}
for i in range(len(exams)):
    exam[exams[i]] = {'id': i+1, 'day_of_exam': exams[i][0], 'starting': exams[i][1], 'ending': exams[i][2], 'course_code': exams[i][3], 'course_name': exams[i][4], 'room_name': exams[i][5], 'room_description': exams[i][6], 'building': exams[i][7]}

exams_insert = "insert into original_exams (id, day_of_exam, starting, ending, course_code, course_name, room_name, room_description, building) values({},'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"

if write_sql_insert_statements_to_file:
    f = open('insert_statements.sql', 'w')

    for k,v in exam.items():
        f.write(exams_insert.format(v['id'], v['day_of_exam'], v['starting'], v['ending'], v['course_code'], v['course_name'], v['room_name'], v['room_description'], v['building']))
        f.write('\n')

    f.close()

if insert_directly_into_database:
    for k,v in exam.items():
        cursor.execute(exams_insert.format(v['id'], v['day_of_exam'], v['starting'], v['ending'], v['course_code'], v['course_name'], v['room_name'], v['room_description'], v['building']))

    conn.commit()

    cursor.close()
    conn.close()