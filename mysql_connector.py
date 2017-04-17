import sys
import mysql.connector
import datetime

if __name__ == "__main__":
    arrv_dept = sys.argv[1]
    year = int(sys.argv[2])

    start = datetime.date(year, 01, 01)
    next = datetime.date(year+1, 01, 01)

    cnx = mysql.connector.connect(user='inf551', password='inf551', host='127.0.0.1', database='inf551')
    cursor = cnx.cursor()

    cursor.execute("""
            select SUM(passenger_count) from LAX
            where arrv_dept = %s and report_period >= %s and report_period < %s
        """, (arrv_dept, start, next))

    for count in cursor:
        print(count[0])
