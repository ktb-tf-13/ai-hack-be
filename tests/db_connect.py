import pymysql

try:
    connection = pymysql.connect(
        host='localhost',  # 또는 실제 호스트
        port=3306,
        user='user',
        password='user',
        database='backend',
        charset='utf8mb4'
    )
    print("연결 성공!")
    connection.close()
except Exception as e:
    print(f"연결 실패: {e}")