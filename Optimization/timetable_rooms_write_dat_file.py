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

thetimeslot = 1

cursor.execute( select_courses.format(solution_id, thetimeslot))
thecourses = cursor.fetchall()

cursor.execute( select_rooms)
therooms = cursor.fetchall()


course_database_to_glpk = {}
course_glpk_to_database = {}

counter = 1
for i in thecourses:
    course_database_to_glpk[i[0]] = counter
    course_glpk_to_database[counter] = i[0]
    counter = counter + 1

room_database_to_glpk = {}
room_glpk_to_database = {}
counter = 1
for i in therooms:
    room_database_to_glpk[i[0]] = counter
    room_glpk_to_database[counter] = i[0]
    counter = counter + 1


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
f.write(';\n')
f.write('end;\n')

conn.close()

# Save the datastructures
pickle_out = open("timetables_rooms_info.pickle","wb")
pickle.dump(course_database_to_glpk, pickle_out)
pickle.dump(course_glpk_to_database, pickle_out)
pickle.dump(room_database_to_glpk, pickle_out)
pickle.dump(room_glpk_to_database, pickle_out)
pickle_out.close()

print('success!!!')

