import os
import sys

import ujson
import mysql.connector
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..")))

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'cowtrack.settings')


with open("./data/salesmetrics_supervisorbranchhistory.json", "r") as f:
    data = f.read()

json_data = ujson.loads(data)

conn = mysql.connector.connect(
    user="root", host="127.0.0.1", port=3306, password="")
cursor = conn.cursor()
cursor.execute("USE cowtrack")

for i in tqdm(range(0, len(json_data))):
    id = json_data[i].get("id")
    supervisor_id = json_data[i].get("supervisor_id")
    branch_id = json_data[i].get("branch_id")
    start_date = json_data[i].get("start_date")
    end_date = json_data[i].get("end_date")

    update_sql = f"""INSERT INTO 
                salesmetrics_supervisorbranchhistory (id, supervisor_id, branch_id, start_date, end_date) 
                VALUES ({id}, {supervisor_id}, {branch_id}, '{start_date}', '{end_date}')"""
    print(update_sql)

    cursor.execute(update_sql)

conn.commit()
cursor.close()
conn.close()

print('supervisorbranchhistory updated')
