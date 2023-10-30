import os
import sys

from django.contrib.auth.hashers import make_password
import ujson
import mysql.connector
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..")))

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'cowtrack.settings')


with open("./data/core_users.json", "r") as f:
    data = f.read()

json_data = ujson.loads(data)
output_file = "update_sql.sql"

conn = mysql.connector.connect(
    user="root", host="127.0.0.1", port=3306, password="")
cursor = conn.cursor()
cursor.execute("USE cowtrack")

for i in tqdm(range(0, len(json_data))):
    password = json_data[i].get("password")
    id = json_data[i].get("id")

    hashed_password = make_password(password)
    update_sql = f"UPDATE core_user SET password = '{hashed_password}' WHERE id = {id};"

    cursor.execute(update_sql)

conn.commit()
cursor.close()
conn.close()

print('Passwords updated')
