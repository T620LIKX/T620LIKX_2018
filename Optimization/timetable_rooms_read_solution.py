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
pickle_in = open("timetables_rooms_info.pickle","rb")
course_database_to_glpk = pickle.load(pickle_in)
course_glpk_to_database = pickle.load(pickle_in)
room_database_to_glpk = pickle.load(pickle_in)
room_glpk_to_database = pickle.load(pickle_in)
pickle_in.close()

the_solution_file = open('timetable_rooms.sol','r')
the_solution = the_solution_file.readlines()
the_solution_file.close()

insert_solution = "insert into solutions_room_assignment () values ();"

for t in the_solution:
    t = t.strip()
    if t.startswith('x') and t.endswith('1'):
        course_id = int(t.split('(')[1].split(')')[0].split(',')[0])
        room_id = int(t.split('(')[1].split(')')[0].split(',')[1])
        database_course_id = course_glpk_to_database[ course_id ]
        database_room_id = room_glpk_to_database[ room_id ]
        cursor.execute(insert_solution.format())

conn.commit()
conn.close()



