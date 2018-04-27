import pickle
import psycopg2

semestercode = 20171
departments = '3,4'

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

select_course_ids = """select c.id, count(e.student_id), c.computer_exam
from courses c, enrollment e
where semester_type = {} and department_id in ({})
and c.id = e.course_id
group by c.id
order by id;"""

select_conflicts = """select tmp.course1, tmp.course2, count(tmp.student_id) 
from (select e1.student_id as student_id, e1.course_id as course1, e2.course_id as course2
      from enrollment e1, enrollment e2, courses c1, courses c2
      where e1.student_id = e2.student_id
      and e1.course_id < e2.course_id
      and e1.course_id = c1.id and e2.course_id = c2.id
      and c1.semester_type = c2.semester_type
      and c2.semester_type = {}
      and c1.department_id in ({}) and c2.department_id in ({})) tmp
group by tmp.course1, tmp.course2
order by tmp.course1, tmp.course2;"""

cursor.execute( select_course_ids.format(semestercode, departments))
thecoursedata = cursor.fetchall()

cursor.execute( select_conflicts.format(semestercode, departments,departments) )
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

fixedcoursesfile = open('examt_fixedcourses.txt')
fixedcourses =fixedcoursesfile.readlines()
fixedcoursesfile.close()

notallowedfile = open('examt_notallowed.txt')
notallowed = notallowedfile.readlines()
notallowedfile.close()


#FASTAR
T = 20
C = len(thecoursedata)
S = 100
N = 829

P1 = 1000
P2 = 500
P3 = 100
P4 = 50
P5 = 40
P6 = 10

f = open('proftafla_test1.dat','w')

f.write('param T := {};\n'.format(T));
f.write('param C := {};\n'.format(C));
f.write('param S := {};\n'.format(S));
f.write('param N := {};\n'.format(N));

f.write('param P1 := {};\n'.format(P1));
f.write('param P2 := {};\n'.format(P2));
f.write('param P3 := {};\n'.format(P3));
f.write('param P4 := {};\n'.format(P4));
f.write('param P5 := {};\n'.format(P5));
f.write('param P6 := {};\n'.format(P6));


f.write('param Courses :=\n')
for i in range(len(thecoursedata)):
    for j in range(len(thecoursedata)):
        if i != j:
            f.write('{} {} {}\n'.format( i+1, j+1, conflict_matrix[i+1][j+1] ))
f.write(';\n')

f.write('param FjoldiNemenda :=\n')
counter = 1
for i in thecoursedata:
    f.write('{} {}\n'.format(counter, i[1]))
    counter = counter + 1
f.write(';\n')

f.write('set FixedCourses :=\n')
for x in fixedcourses:
    course_id = x.split()[0]
    timeslot = x.split()[1]
    includethiscourse = False
    for i in thecoursedata:
        if i[0] == course_id:
            includethiscourse = True
        if includethiscourse:
            f.write('{} {}\n'.format(id_database_to_glpk[course_id], timeslot))
f.write(';\n')

f.write('set NotAllowed :=\n')
for x in notallowed:
    course_id = x.split()[0]
    timeslot = x.split()[1]
    includethiscourse = False
    for i in thecoursedata:
        if i[0] == course_id:
            includethiscourse = True
    if includethiscourse:
        f.write('{} {}\n'.format(id_database_to_glpk[course_id], timeslot))
f.write(';\n')

f.write('set ComputerExam :=\n')
counter = 1
for i in thecoursedata:
    if i[2] == True:
      f.write('{}\n'.format(counter))
    counter = counter + 1
f.write(';\n')

f.write('end;\n')

f.close()

conn.close()

# Save the datastructures
pickle_out = open("examtables_course_ids.pickle","wb")
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

print("Run successful!!!")
