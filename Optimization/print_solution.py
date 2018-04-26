import psycopg2
import sys

default_slots = {'timetable': 4, 'examtable': 2}
default_days = {'timetable': 4, 'examtable': 10}


def leftpad(s,w,padding=' '):
    return padding*(w-len(s))+s

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

def create_table(sol, department = ''):
    solution_type = sol[0][4]
    slots = default_slots[solution_type]
    days = default_days[solution_type]

    thetable = [[ [] for _ in range(slots)] for _ in range(days)]

    for s in sol:
        if department == '' or s[2] == department:
            thetimeslot = (s[3]-1) % slots
            theday = (s[3]-1) // slots

            thetable[theday][thetimeslot].append(s[1])

    return thetable, slots, days


def print_solution(timetable, slots, days):
    fieldwidth = 0
    fieldheight = 0
    for i in range(days):
        for j in range(slots):
            for k in thetable[i][j]:
                fieldwidth = max(fieldwidth, len(k))
            fieldheight = max(fieldheight, len(thetable[i][j]))


    print(leftpad('-',3+(fieldwidth+1)*days,padding='-'))
    for timeslot in range(slots):
        for i in range(fieldheight):
            for d in range(days):
                print('|',end='')
                if d == days//2:
                    print('-|',end='')

                if i < len(thetable[d][timeslot]):
                    print(leftpad(thetable[d][timeslot][i],fieldwidth), end='')
                else:
                    print(leftpad(' ',fieldwidth), end='')
            print('|')
        print(leftpad('-',3+(fieldwidth+1)*days,padding='-'))

#-------------------------------------

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

select_solution = """select s.course_id, c.course_code, d.department_name, s.timeslot, s.solution_type
from solutions s, courses c, departments d
where s.course_id = c.id and c.department_id = d.id
and s.solution_id = {}
order by d.department_name, s.timeslot, s.course_id;"""

cursor.execute(select_solution.format(solution_id))
thesolutions = cursor.fetchall()
conn.close()

if len(thesolutions) == 0:
    print('No solution found')
    exit()

departments = set()
for s in thesolutions:
    departments.add(s[2])
departments = list(departments)
departments.sort()

print('Departments: {}'.format(', '.join(departments)))
thetable, slots, days = create_table(thesolutions)
print_solution(thetable, slots, days)

if len(departments) > 1:
    print('')
    print('')
    for d in departments:
        print('Department: {}'.format(d))
        thetable, slots, days = create_table(thesolutions, department=d)
        print_solution(thetable, slots, days)
        print('')
        print('')


