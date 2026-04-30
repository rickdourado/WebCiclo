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
        if p['Command'] != 'Sleep' and p['Info'] and 'SHOW FULL PROCESSLIST' not in p['Info']:
            print(f"Killing process {p['Id']} - {p['Info']}")
            cursor.execute(f"KILL {p['Id']}")
        elif p['Command'] == 'Sleep' and p['Time'] > 60:
            print(f"Killing sleeping process {p['Id']}")
            cursor.execute(f"KILL {p['Id']}")
