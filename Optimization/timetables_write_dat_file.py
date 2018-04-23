import pickle
import psycopg2

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


def calculate_conflict_penalty(c):
    return c


cursor, conn = connect_to_database('localhost', 'likanx','postgres', 'postgres')

select_course_ids = """select id
from courses
where semester_type = {} and department_id = {}
order by id;"""

select_conflicts = """select tmp.course1, tmp.course2, count(tmp.student_id)
from (select e1.student_id as student_id, e1.course_id as course1, e2.course_id as course2
      from enrollment e1, enrollment e2, courses c1, courses c2
      where e1.student_id = e2.student_id
      and e1.course_id < e2.course_id
      and e1.course_id = c1.id and e2.course_id = c2.id
      and c1.semester_type = c2.semester_type
      and c2.semester_type = {}
      and c1.department_id = {} and c2.department_id = {}) tmp
group by tmp.course1, tmp.course2
order by tmp.course1, tmp.course2;"""

cursor.execute( select_course_ids.format(20171,4))
thecoursedata = cursor.fetchall()

cursor.execute( select_conflicts.format(20171, 4, 4) )
thedata = cursor.fetchall()

id_database_to_glpk = {}
id_glpk_to_database = {}

counter = 1
for i in thecoursedata:
    id_database_to_glpk[i[0]] = counter
    id_glpk_to_database[counter] = i[0]
    counter = counter + 1

conflict_matrix = [[0 for _ in range(1+len(thecoursedata))] for _ in range(1+len(thecoursedata))]

for i in thedata:
    course_1 = id_database_to_glpk[ i[0] ]
    course_2 = id_database_to_glpk[ i[1] ]
    conflict_penalty = calculate_conflict_penalty(i[2])
    conflict_matrix[course_1][course_2] = conflict_penalty
    conflict_matrix[course_2][course_1] = conflict_penalty


#FASTAR
T = 16
C = len(thecoursedata)
S = 100

f = open('stundatafla_test1.dat','w')

f.write('param T := {};\n'.format(T));
f.write('param C := {};\n'.format(C));
f.write('param S := {};\n'.format(S));

f.write('param K:=\n')
for i in range(len(thecoursedata)):
    for j in range(len(thecoursedata)):
        if i != j:
            f.write('{} {} {}\n'.format( i+1, j+1, conflict_matrix[i+1][j+1] ))
f.write(';\n')

f.write('param P:=\n')
for i in range(C):
    for j in range(T):
        f.write('{} {} 0\n'.format(i+1,j+1))
f.write(';\n')

f.write('end;\n')

f.close()

conn.close()

# Save the datastructures
pickle_out = open("timetables_course_ids.pickle","wb")
pickle.dump(id_database_to_glpk, pickle_out)
pickle.dump(id_glpk_to_database, pickle_out)
pickle_out.close()

"""
# Load the datastructures
pickle_in = open("course_ids.pickle","rb")
id_database_to_glpk = pickle.load(pickle_in)
id_glpk_to_database = pickle.load(pickle_in)
pickle_in.close()
"""

