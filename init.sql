-- 1. 기본 데이터베이스 (docker-compose 환경변수용)
CREATE DATABASE IF NOT EXISTS myapp;
USE myapp;

-- 2. 새로운 테스트 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS backend;
USE backend;

-- 3. 새로운 사용자 생성 및 권한 부여
-- 'test_user'가 모든 호스트(%)에서 접속 가능하도록 설정
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'user';
GRANT ALL PRIVILEGES ON backend.* TO 'user'@'%';
FLUSH PRIVILEGES;

-- User 테이블
CREATE TABLE User (
    user_id VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NULL,
    is_answered BOOLEAN NOT NULL DEFAULT false,
    goal_content TEXT NULL,
    PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Challenge 테이블
CREATE TABLE Challenge (
    challenge_id BIGINT NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL,
    challenge_content VARCHAR(255) NOT NULL,
    challenge_is_checked BOOLEAN NOT NULL DEFAULT false,
    challenge_date DATE NOT NULL,
    PRIMARY KEY (challenge_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Record 테이블
CREATE TABLE Record (
    record_id BIGINT NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL,
    record_content VARCHAR(255) NULL,
    record_is_wrote BOOLEAN NOT NULL DEFAULT false,
    record_date DATE NOT NULL,
    PRIMARY KEY (record_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 인덱스 추가 (성능 최적화)
CREATE INDEX idx_challenge_user_date ON Challenge(user_id, challenge_date);
CREATE INDEX idx_record_user_date ON Record(user_id, record_date);
-- 주간 리포트 테이블
CREATE TABLE WeeklyReport (
    report_id BIGINT NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    week INT NOT NULL,
    summary TEXT NOT NULL,
    feedback TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (report_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 온보딩 세션 테이블
CREATE TABLE OnboardingSession (
    session_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(255) NULL,
    current_step INT DEFAULT 0,
    history_data JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (session_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

commit;