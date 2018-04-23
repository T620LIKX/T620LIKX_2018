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


cursor, conn = connect_to_database('localhost', 'likanx','postgres', 'postgres')

# Load the datastructures
pickle_in = open("examtables_course_ids.pickle","rb")
id_database_to_glpk = pickle.load(pickle_in)
id_glpk_to_database = pickle.load(pickle_in)
pickle_in.close()

the_solution_file = open('proftafla.sol','r')
the_solution = the_solution_file.readlines()
the_solution_file.close()

solution_id = 1
select_max_solution_id = "select max(solution_id) from solutions;"
cursor.execute(select_max_solution_id)
max_solution_id = cursor.fetchall()
if max_solution_id[0][0] is not None:
    solution_id = 1 + max_solution_id[0][0]

insert_solution = "insert into solutions (solution_id, solution_type, course_id, timeslot) values ({},'examtable',{},{});"

for t in the_solution:
    t = t.strip()
    if t.startswith('x') and t.endswith('1'):
        course_id = int(t.split('(')[1].split(')')[0].split(',')[0])
        database_course_id = id_glpk_to_database[ course_id ]
        timeslot = int(t.split('(')[1].split(')')[0].split(',')[1])
        #print('Course {} is in timeslot {}'.format(database_course_id, timeslot))
        cursor.execute(insert_solution.format(solution_id, database_course_id, timeslot))

conn.commit()
conn.close()
