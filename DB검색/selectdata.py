import psycopg2
import time

conn = psycopg2.connect(
    host='localhost',
    dbname='test_db',  
    user='postgres',
    password='password',
    port=5432
)


cursor = conn.cursor()

A = time.time()
sql = """
    select * from flight_tickets where (departure_time between '2025-03-12' and '2025-03-13' and departure_airport='GMP' and arrival_airport ='CJU' )
"""

cursor.execute(sql)

rows = cursor.fetchall()
B = time.time()
print(B-A)

# for i in rows:
#     print(i)

cursor.close()
conn.close()