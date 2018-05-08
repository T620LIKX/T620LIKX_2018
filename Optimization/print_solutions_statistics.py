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

def create_table_exams(sol):
    solution_type = 'examtable'
    slots = default_slots[solution_type]
    days = default_days[solution_type]

    thetable = [[ 0 for _ in range(slots)] for _ in range(days)]

    for s in sol:
        thetimeslot = (s[0]-1) % slots
        theday = (s[0]-1) // slots

        thetable[theday][thetimeslot] += s[1]

    return thetable, slots, days

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
    fieldheight = 1
    for i in range(days):
        for j in range(slots):
            fieldwidth = max(fieldwidth, len(str(thetable[i][j])))


    print(leftpad('-',3+(fieldwidth+1)*days,padding='-'))
    for timeslot in range(slots):
        for d in range(days):
            print('|',end='')
            if d == days//2:
                print('-|',end='')

            print(leftpad(str(thetable[d][timeslot]),fieldwidth), end='')
        print('|')
    print(leftpad('-',3+(fieldwidth+1)*days,padding='-'))


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

print_details = False
if len(sys.argv) > 2:
    if sys.argv[2] == '1':
        print_details = True


# Er þetta próftöflulausn?
proftafla = False
proftafla_check = """select * from solutions
where solution_id = {}
and solution_type = 'examtable';"""

cursor.execute(proftafla_check.format(solution_id))
total_proftafla_check = cursor.fetchall()

if len(total_proftafla_check) > 0:
    proftafla = True

# Er þetta stundatöflulausn?
stundatafla = False
stundatafla_check = """select * from solutions
where solution_id = {}
and solution_type = 'timetable';"""

cursor.execute(stundatafla_check.format(solution_id))
total_stundatafla_check = cursor.fetchall()

if len(total_stundatafla_check) > 0:
    stundatafla = True

# Proftöflu prentun
if proftafla == True:
    students_in_timeslot = """select s.timeslot, count(e.student_id)
    from courses c, enrollment e, solutions s
    where solution_id = {}
    and c.id = s.course_id
    and c.id = e.course_id
    group by s.timeslot
    order by s.timeslot;"""

    cursor.execute(students_in_timeslot.format(solution_id))
    total_students_in_timeslot = cursor.fetchall()

    headline = "Fjöldi nemenda í prófi í hverju tímaslotti:"
    print(headline)
    thetable, slots, days = create_table_exams(total_students_in_timeslot)
    print_solution(thetable, slots, days)


    total_students = """ select count(student_id) from
      (SELECT DISTINCT e.student_id
    FROM enrollment e, courses c, solutions s
    WHERE s.solution_id = 2
    AND e.course_id = s.course_id
    AND e.course_id = c.id
    GROUP BY e.student_id
    ORDER BY e.student_id) tmp"""

    cursor.execute(total_students.format(solution_id))
    total_students_in_table= cursor.fetchall()

    print('Heildarfjöldi nemenda sem skráðir eru í lokapróf:', total_students_in_table[0][0])

    #skörun í sama tímaslotti

    student_skorun = """select e1.student_id, c1.course_code, c2.course_code, s1.timeslot
    from enrollment e1, enrollment e2, courses c1, courses c2, solutions s1, solutions s2
    where s1.solution_id = {}
    and s2.solution_id = s1.solution_id
    and e1.student_id = e2.student_id
    and e1.course_id < e2.course_id
    and e1.course_id = s1.course_id and e2.course_id = s2.course_id
    and e1.course_id = c1.id and e2.course_id = c2.id
    and s1.timeslot = s2.timeslot
    group by e1.student_id, c1.course_code, c2.course_code, s1.timeslot
    order by e1.student_id"""

    cursor.execute(student_skorun.format(solution_id))
    total_students_skorun = cursor.fetchall()


    if len(total_students_skorun) == 0:
        print('Enginn nemandi er skráður í tvö próf á sama tíma.')

    else:
        counter = 0
        for x in total_students_skorun:
            counter += 1

        print('Fjöldi nemenda sem skráðir eru í próf í sama tímaslotti:', counter)


    #próf fyrir og eftir hádegi

    student_skorun_fyrir_og_eftir_hadegi = """select e1.student_id, c1.course_code, s1.timeslot, c2.course_code, s2.timeslot
    from enrollment e1, enrollment e2, courses c1, courses c2, solutions s1, solutions s2
    where s1.solution_id = {}
    and s2.solution_id = s1.solution_id
    and e1.student_id = e2.student_id
    and e1.course_id < e2.course_id
    and e1.course_id = s1.course_id and e2.course_id = s2.course_id
    and e1.course_id = c1.id and e2.course_id = c2.id
    and s1.timeslot + 1 = s2.timeslot
    and s2.timeslot%2 = 0
    group by e1.student_id, c1.course_code, s1.timeslot, c2.course_code, s2.timeslot
    order by e1.student_id"""


    cursor.execute(student_skorun_fyrir_og_eftir_hadegi.format(solution_id))
    total_student_skorun_fyrir_og_eftir_hadegi = cursor.fetchall()

    counter = 0
    for x in total_student_skorun_fyrir_og_eftir_hadegi:
        counter +=1

    print('Fjöldi nemenda sem eru skráðir í próf fyrir og eftir hádegi sama dags: ', counter)

    select_solution = """select s.course_id, c.course_code, d.department_name, s.timeslot, s.solution_type, e.student_id
    from solutions s, courses c, departments d, enrollment e
    where s.course_id = c.id and c.department_id = d.id and c.id = e.course_id
    and s.solution_id = {} and e.student_id = {}
    order by d.department_name, s.timeslot, s.course_id, e.student_id;"""


    select_students = """select e.student_id
    from enrollment e, solutions s, courses c
    where s.course_id = c.id and c.id = e.course_id
    and s.solution_id = {}
    group by e.student_id;"""

    cursor.execute(select_students.format(solution_id))
    thestudents = cursor.fetchall()

    fjoldi_nem_2daga_i_rod = 0
    fjoldi_nem_3daga_i_rod = 0
    fjoldi_nem_4daga_i_rod = 0
    fjoldi_nem_5daga_i_rod = 0

    for i in thestudents:
        cursor.execute(select_solution.format(solution_id, i[0]))
        thesolutions = cursor.fetchall()

        thetable, slots, days = create_table(thesolutions)

        this_student_is_3days_in_row = False
        for theday in [0,1,2,5,6,7]:
            if (len(thetable[theday][0]+thetable[theday][1]) > 0) and (len(thetable[theday+1][0]+thetable[theday+1][1]) > 0) and (len(thetable[theday+2][0]+thetable[theday+2][1]) > 0):
                this_student_is_3days_in_row = True

        if this_student_is_3days_in_row:
            fjoldi_nem_3daga_i_rod += 1

            #print_solution(thetable, slots, days)

        this_student_is_4days_in_row = False
        for theday in [0,1,5,6]:
            if (len(thetable[theday][0]+thetable[theday][1]) > 0) and (len(thetable[theday+1][0]+thetable[theday+1][1]) > 0) and (len(thetable[theday+2][0]+thetable[theday+2][1]) > 0) and (len(thetable[theday+3][0]+thetable[theday+3][1]) > 0):
                this_student_is_4days_in_row = True

        if this_student_is_4days_in_row:
            fjoldi_nem_4daga_i_rod += 1

            #print_solution(thetable, slots, days)

        this_student_is_5days_in_row = False
        for theday in [0,5]:
            if (len(thetable[theday][0]+thetable[theday][1]) > 0) and (len(thetable[theday+1][0]+thetable[theday+1][1]) > 0) and (len(thetable[theday+2][0]+thetable[theday+2][1]) > 0) and (len(thetable[theday+3][0]+thetable[theday+3][1]) > 0) and (len(thetable[theday+4][0]+thetable[theday+4][1]) > 0):
                this_student_is_5days_in_row = True

        if this_student_is_5days_in_row:
            fjoldi_nem_5daga_i_rod += 1

            #print_solution(thetable, slots, days)

        this_student_is_2days_in_row = False
        for theday in [0,1,2,3,5,6,7,8]:
            if (len(thetable[theday][0]+thetable[theday][1]) > 0) and (len(thetable[theday+1][0]+thetable[theday+1][1]) > 0):
                this_student_is_2days_in_row = True

        if this_student_is_2days_in_row:
            fjoldi_nem_2daga_i_rod += 1

            #print_solution(thetable, slots, days)


    print('Fjöldi nemenda í tveimur eða fleiri prófum 2 daga í röð: {}'.format(fjoldi_nem_2daga_i_rod))
    print('Fjöldi nemenda í þremur eða fleiri prófum 3 daga í röð: {}'.format(fjoldi_nem_3daga_i_rod))
    print('Fjöldi nemenda í fjórum eða fleiri prófum 4 daga í röð: {}'.format(fjoldi_nem_4daga_i_rod))
    print('Fjöldi nemenda í fimm eða fleiri prófum 5 daga í röð: {}'.format(fjoldi_nem_5daga_i_rod))


    #Fjöldi nemenda í hverju lokaprófi
    if print_details == True:
        student_taking_exam = """select c.course_code, c.course_name, s.timeslot, count(e.student_id)
        from courses c, enrollment e, solutions s
        where solution_id = {}
        and c.id = s.course_id
        and c.id = e.course_id
        group by c.course_code, c.course_name, s.timeslot
        order by s.timeslot;"""

        cursor.execute(student_taking_exam.format(solution_id))
        total_students_taking_exam = cursor.fetchall()

        print('\n')
        print('Fjöldi nemenda í hverju lokaprófi')
        for x in total_students_taking_exam:
            print(x[0], '-', x[1], '- fjöldi nemanda:', x[3])

        print('\n')
        print('Nemendur sem skráðir eru í tvö próf á sama tíma:')
        for x in total_students_skorun:
            print('Student ID:', x[0], '- áfangar sem skarast:', x[1], 'og', x[2], '- tímaslott:', x[3])

        print('\n')
        print('Nemendur sem skráðir eru í próf fyrir og eftir hádegi sama dags:')
        for x in total_student_skorun_fyrir_og_eftir_hadegi:
            print('Student ID: ', x[0], '- áfangar sem skarast:' ,x[1] , 'og', x[3], '- tímaslott:', x[2], 'og', x[4])

elif stundatafla == True:
    
    student_skorun = """select e1.student_id, c1.course_code, c2.course_code, s1.timeslot
    from enrollment e1, enrollment e2, courses c1, courses c2, solutions s1, solutions s2
    where s1.solution_id = {}
    and s2.solution_id = s1.solution_id
    and e1.student_id = e2.student_id
    and e1.course_id < e2.course_id
    and e1.course_id = s1.course_id and e2.course_id = s2.course_id
    and e1.course_id = c1.id and e2.course_id = c2.id
    and s1.timeslot = s2.timeslot
    group by e1.student_id, c1.course_code, c2.course_code, s1.timeslot
    order by e1.student_id"""

    cursor.execute(student_skorun.format(solution_id))
    total_students_skorun = cursor.fetchall()

    if len(total_students_skorun) == 0:
        print('Engin nemandi er skráður í tvo áfanga á sama tíma.')
    else:
        counter = 0
        for x in total_students_skorun:
            counter += 1
        print('Fjöldi nemenda sem skráðir eru í fleiri en einn áfanga sem kenndir eru í sama tímaslotti:', counter)

    nem_i_gati = """ select e1.student_id, c1.course_code, s1.timeslot, c2.course_code, s2.timeslot
    from enrollment e1, enrollment e2, courses c1, courses c2, solutions s1, solutions s2
    where s1.solution_id = {}
    and s2.solution_id = s1.solution_id
    and e1.student_id = e2.student_id
    and e1.course_id = s1.course_id and e2.course_id = s2.course_id
    and e1.course_id = c1.id and e2.course_id = c2.id
    and s1.timeslot + 3 = s2.timeslot
    and s2.timeslot % 4 = 0
    group by e1.student_id, c1.course_code, s1.timeslot, c2.course_code, s2.timeslot
    order by e1.student_id"""

    cursor.execute(nem_i_gati.format(solution_id))
    total_nem_i_gati = cursor.fetchall()


    if len(total_nem_i_gati) == 0:
        print('Enginn nemandi er í gati á milli 10:05 og 14:00.')
    else:
        counter = 0
        for x in total_nem_i_gati:
            counter += 1
        print('Fjöldi nemenda sem skráðir eru einhvern dag vikunnar í gati á milli 10:05 og 14:00 :', counter)

        if print_details == True:
            for x in total_nem_i_gati:
                if x[2] == 1:
                    dagur = 'mánudegi'
                if x[2] == 5:
                    dagur = 'þriðjudegi'
                if x[2] == 9:
                    dagur = 'fimmtudegi'
                if x[2] == 13:
                    dagur = 'föstudegi'
                print('nemandi nr: ', x[0], 'er í gati á milli 10:05 og 14:00 á', dagur)


else:
    print('No solution found')
    exit()



    conn.close()

