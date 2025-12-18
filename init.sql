-- 1. 기본 데이터베이스 (docker-compose 환경변수용)
CREATE DATABASE IF NOT EXISTS myapp;
USE myapp;

-- 2. 새로운 테스트 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS backend;

-- 3. 새로운 사용자 생성 및 권한 부여
-- 'test_user'가 모든 호스트(%)에서 접속 가능하도록 설정
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'user';
GRANT ALL PRIVILEGES ON backend.* TO 'user'@'%';
FLUSH PRIVILEGES;

-- 4. 테스트용 임시 테이블 생성 (test_db 사용)
CREATE TABLE IF NOT EXISTS backend.User (
    user_id VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(100) NOT NULL,
    img_id VARCHAR(50)
);

INSERT INTO User (user_id, password, nickname, img_id) VALUES 
('testuser', 'password123', '테스트유저', NULL);
