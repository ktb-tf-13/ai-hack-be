# 1. Python 3.11 슬림 버전 사용
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 전체 코드 복사
COPY . .
ENV PYTHONPATH=/app

# 5. 서버 실행 명령어 
# --host 0.0.0.0 은 외부 접속을 허용
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]