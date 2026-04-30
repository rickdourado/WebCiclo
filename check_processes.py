import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 3308)),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', ''),
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    cursor.execute("SHOW FULL PROCESSLIST")
    processes = cursor.fetchall()
    for p in processes:
        if p['Command'] != 'Sleep':
            print(f"Id: {p['Id']}, User: {p['User']}, Host: {p['Host']}, db: {p['db']}, Command: {p['Command']}, Time: {p['Time']}, State: {p['State']}, Info: {p['Info']}")
