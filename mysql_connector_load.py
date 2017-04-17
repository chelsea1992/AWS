import json
import sys
import mysql.connector
from datetime import datetime

if __name__ == "__main__":
    json_file = sys.argv[1]
    json_data = json.load(open(json_file))['data']

    cnx = mysql.connector.connect(user='inf551', password='inf551', host='127.0.0.1', database='inf551')
    cursor = cnx.cursor()

    add_info = ("INSERT INTO LAX"
                "(report_period, terminal, arrv_dept, dom_inter, passenger_count) "
                "VALUES (%s, %s, %s, %s, %s)")

    for item in json_data:
        oneDoc = (
            datetime.strptime(item[9], "%Y-%m-%dT%H:%M:%S"),
            item[10],
            item[11],
            item[12],
            int(item[13])
        )
        cursor.execute(add_info, oneDoc)

cnx.commit()

cursor.close()
cnx.close()
