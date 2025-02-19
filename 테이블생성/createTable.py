import psycopg2

# PostgreSQL 서버에 기본적으로 연결 (postgres 데이터베이스 사용)
conn = psycopg2.connect(
    host='localhost',
    dbname='test_db',  
    user='postgres',
    password='password',
    port=5432
)
conn.autocommit = True  # 트랜잭션 자동 커밋 설정
cursor = conn.cursor()
sql ="""
    CREATE TABLE test_db (
        id SERIAL PRIMARY KEY,
        departure_time TIMESTAMP NOT NULL,
        arrival_time TIMESTAMP NOT NULL,
        price NUMERIC(10,2) NOT NULL,
        seats_available INT NOT NULL,
        departure_airport VARCHAR(10) NOT NULL,
        arrival_airport VARCHAR(10) NOT NULL,
        airline_codes VARCHAR(10) NOT NULL
    );
"""
cursor.execute(sql)

cursor.close()
conn.close()
