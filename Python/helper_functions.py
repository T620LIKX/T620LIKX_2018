from datetime import datetime
import psycopg2
import csv

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

def get_data(filename, delimiter=';'):
    file = open(filename, encoding = 'utf-8')
    reader = csv.DictReader(file, delimiter=delimiter)
    data = []
    for row in reader:
        data.append(row)
    file.close()
    return data

def fix_date_style(i):
    i['Course_Starts'] = i['Course_Starts'].replace("/", "-")
    i['Course_Ends'] = i['Course_Ends'].replace("/", "-")

def get_date_v1(d):
    # Here we assume that the date is something like '16/08/17 00:00:00.000'
    tmp = d.split()
    tmp1 = tmp[0]
    t = tmp1.split('/')
    thedate = '20' + t[2] + '-' + t[1] + '-' + t[0]
    return thedate

def get_date_v2(d):
    # Here we assume that the date is something like '2017-08-16 00:00:00.000'
    if d == 'NULL':
        return '2000-01-01'
    tmp = d.split()
    return tmp[0]


def get_semester_type(d1,d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    date1 = d1.date()
    date2 = d2.date()
    diffweeks = abs((date2 - date1).days / 7)

    if diffweeks <= 14 and diffweeks >= 11 and date1.month >= 8:
        semester_type_code = 1 #fall semester 12 weeks
    elif diffweeks < 4 and diffweeks > 2 and date1.month >= 8:
        semester_type_code = 2 #fall semester 3 weeks
    elif diffweeks > 14 and diffweeks < 17 and date1.month >= 8:
        semester_type_code = 3 #fall semester 15 weeks
    elif diffweeks <= 14 and diffweeks >= 11 and date1.month <= 6:
        semester_type_code = 4 #spring semester 12 weeks
    elif diffweeks < 4 and diffweeks > 2 and date1.month <= 6:
        semester_type_code = 5 #spring semester 3 weeks
    elif diffweeks > 14 and diffweeks < 17 and date1.month <= 6:
        semester_type_code = 6 #spring semester 15 weeks
    else:
        semester_type_code = 9
    return date1.year * 10 + semester_type_code


def calculate_lectures_per_week(semester_type, l_count):
    s_type = semester_type % 10

    if s_type == 1 or s_type == 4:
        l_per_week = l_count/12
    elif s_type == 2 or s_type == 5:
        l_per_week = l_count/3
    elif s_type == 3 or s_type == 6:
        l_per_week = l_count/15
    elif s_type == 9:
        l_per_week = 0 # semester type 9 is unknown so we assume there are no lectures in this course

    return int(l_per_week + 0.2)  # Approximate the correct number of lectures per week, add 0.2 so that 1.9 becomes 2 lectures per week.
