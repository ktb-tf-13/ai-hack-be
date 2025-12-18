import pymysql
import sys
import os

# Add project root to sys.path to import app.config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings

try:
    connection = pymysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        charset='utf8mb4'
    )
    print(f"✅ 연결 성공! (Host: {settings.db_host}, DB: {settings.db_name})")
    connection.close()
except Exception as e:
    print(f"❌ 연결 실패: {e}")