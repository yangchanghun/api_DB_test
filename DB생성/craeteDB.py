import psycopg2

# PostgreSQL 서버에 기본적으로 연결 (postgres 데이터베이스 사용)
conn = psycopg2.connect(
    host='localhost',
    dbname='postgres',  # 기본 DB에 연결
    user='postgres',
    password='password',
    port=5432
)

# 트랜잭션 비활성화 (CREATE DATABASE 실행 가능하도록 설정)
conn.autocommit = True

cursor = conn.cursor()

# CREATE DATABASE 실행
database_name = "test_db"
sql = f"CREATE DATABASE {database_name};"

try:
    cursor.execute(sql)
    print(f"✅ 데이터베이스 {database_name} 생성 완료!")
except psycopg2.errors.DuplicateDatabase:
    print(f"⚠️ 데이터베이스 {database_name} 이미 존재함.")
except Exception as e:
    print(f"❌ 오류 발생: {e}")

# 연결 종료
cursor.close()
conn.close()
