# Backend Project Guide

## 🏗️ 아키텍처
- **Backend**: FastAPI (Python)
- **Database**: MariaDB
- **Package Manager**: uv

## 🛠️ 환경 구성 (Environment Setup)

### 1. `.env` 파일 설정
프로젝트 실행 전 환경 변수 파일을 생성합니다.
```bash
cp .env.example .env
```

### 2. 데이터베이스 실행 (Docker)
MariaDB 컨테이너를 실행합니다. (`init.sql`이 자동으로 실행되어 초기 데이터를 생성합니다.)
```bash
docker compose -f docker-compose.yml up -d
```

> **참고**: DB 초기화 스크립트(`init.sql`)가 수정되었다면, 기존 볼륨을 삭제하고 다시 실행해야 적용됩니다.
> ```bash
> # DB 데이터 초기화 및 재실행
> docker compose down -v
> docker compose -f docker-compose.yml up -d
> ```

---

## 📦 패키지 설치 (Installation)

빠른 속도의 Python 패키지 매니저인 **uv**를 사용합니다.

### 1. uv 설치
```bash
brew install uv
```

### 2. 가상환경 생성 및 의존성 설치
`pyproject.toml`을 기반으로 가상환경을 구성합니다.
```bash
uv sync
```

---

## 🚀 프로젝트 실행 (Execution)

가상환경을 사용하여 백엔드 서버를 실행합니다.
```bash
uv run uvicorn app.main:app --reload
```

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔧 트러블슈팅 (Troubleshooting)

### 데이터베이스 접속 확인
터미널에서 직접 DB에 접속하여 데이터를 확인할 수 있습니다.
```bash
# 1. 컨테이너 접속 (비밀번호: user)
docker exec -it mariadb-db mariadb -u user -p

# 2. DB 및 테이블 조회
MariaDB [(none)]> use backend;
MariaDB [backend]> show tables;
MariaDB [backend]> select * from User;
```

### 가상환경 오류 해결
의존성이 꼬였을 경우 가상환경을 초기화합니다.
```bash
rm -rf .venv
rm -f uv.lock
uv sync
```