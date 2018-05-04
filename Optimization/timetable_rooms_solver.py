from subprocess import call
import psycopg2
import sys
import pickle

def connect_to_database(host, dbname, username, pw):
    conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)
    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.OperationalError as e:
        print('Connection failed!')
        print('Error message:', e)
        exit()
    cursor = conn.cursor()
    return cursor, conn

cursor, conn = connect_to_database('localhost', 'likanx','postgres', 'postgres')

if len(sys.argv) > 1:
    solution_id = int(sys.argv[1])
else:
    select_max_solution_id = "select max(solution_id) from solutions;"
    cursor.execute(select_max_solution_id)
    max_solution_id = cursor.fetchall()
    if max_solution_id[0][0] is not None:
        solution_id = max_solution_id[0][0]
    else:
        solution_id = -1

select_courses = """select s.course_id, count(e.student_id)
from solutions s, enrollment e
where s.solution_id = {}
and s.timeslot = {}
and s.course_id = e.course_id
group by s.course_id
order by s.course_id;"""

select_rooms = """select id, name, seats from rooms
where description like '%ennslustofa%'
or description like '%Málstofa%';"""

insert_solution = "insert into solution_room_assignment (solution_id, timeslot, course_id, room_id, student_count) values ({},{},{},{},{});"

thetimeslot = 1
while thetimeslot <= 16:
    cursor.execute( select_courses.format(solution_id, thetimeslot))
    thecourses = cursor.fetchall()

    cursor.execute( select_rooms)
    therooms = cursor.fetchall()


    course_database_to_glpk = {}
    course_glpk_to_database = {}

    counter = 1
    for i in thecourses:
        course_database_to_glpk[int(i[0])] = counter
        course_glpk_to_database[counter] = int(i[0])
        counter = counter + 1

    room_database_to_glpk = {}
    room_glpk_to_database = {}
    counter = 1
    for i in therooms:
        room_database_to_glpk[int(i[0])] = counter
        room_glpk_to_database[counter] = int(i[0])
        counter = counter + 1

    #ath stadsetningu
    fixedcoursesfile = open('timetable_fixedcourses_rooms.txt')
    fixedcourses =fixedcoursesfile.readlines()
    fixedcoursesfile.close()

    notallowedfile = open('timetable_notallowed_rooms.txt')
    notallowed = notallowedfile.readlines()
    notallowedfile.close()

    C = len(thecourses)
    R = len(therooms)

    f = open('timetable_rooms_test1.dat','w')

    f.write('param C := {};\n'.format(C))
    f.write('param R := {};\n'.format(R))
    f.write('\n')
    f.write('param S :=\n')
    counter = 1
    for s in therooms:
        f.write('{} {}\n'.format(counter, s[2]))
        counter = counter + 1
    f.write(';\n')

    f.write('param N :=\n')
    counter = 1
    for c in thecourses:
        f.write('{} {}\n'.format(counter, c[1]))
        counter = counter + 1
    f.write(';\n')

    f.write('set NotAllowed :=\n')
    for x in notallowed:
        course_id = int(x.split()[0])
        room_id = int(x.split()[1])
        includethiscourse = False
        for i in thecourses:
            if i[0] == course_id:
                includethiscourse = True
        if includethiscourse:
            f.write('{} {}\n'.format(course_database_to_glpk[course_id], room_database_to_glpk[room_id]))
    f.write(';\n')

    f.write('set FixedCourses :=\n')
    for x in fixedcourses:
        course_id = int(x.split()[0])
        room_id = int(x.split()[1])
        includethiscourse = False
        for i in thecourses:
            if i[0] == course_id:
                includethiscourse = True
        if includethiscourse:
            f.write('{} {}\n'.format(course_database_to_glpk[course_id], room_database_to_glpk[room_id]))
    f.write(';\n')
    f.write('end;\n')
    f.close()


    # Keyra bestun
    call(["glpsol", "--math", "-m", "timetable_rooms.mod", "-d", "timetable_rooms_test1.dat", "--check", "--wlp", "timetable_rooms.lp"])
    call(["gurobi_cl", "ResultFile=timetable_rooms.sol", "timetable_rooms.lp"])

    # Lesa lausn
    the_solution_file = open('timetable_rooms.sol','r')
    the_solution = the_solution_file.readlines()
    the_solution_file.close()

    print('-------------------')
    print(course_glpk_to_database)
    print('-------------------')
    print(room_glpk_to_database)
    print('-------------------')

    for t in the_solution:
        t = t.strip()
        if t.startswith('x') and t.endswith('1'):
            course_id = int(t.split('(')[1].split(')')[0].split(',')[0])
            room_id = int(t.split('(')[1].split(')')[0].split(',')[1])
            database_course_id = course_glpk_to_database[ course_id ]
            database_room_id = room_glpk_to_database[ room_id ]
            cursor.execute(insert_solution.format(solution_id, thetimeslot, database_course_id, database_room_id, 1))
    conn.commit()

    thetimeslot = thetimeslot + 1

conn.close()

print('success!!!')

