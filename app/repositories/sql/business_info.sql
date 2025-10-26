-- 사업장정보 테이블 생성 스크립트
-- SQLite 데이터베이스용 DDL

-- 사업장정보 테이블 생성
CREATE TABLE IF NOT EXISTS business_info (
    -- 사업자등록번호 (Primary Key)
    business_registration_number VARCHAR(10) PRIMARY KEY,
    
    -- 사업자명 (필수)
    business_name VARCHAR(255) NOT NULL,
    
    -- 대표자명 (필수)
    representative_name VARCHAR(100) NOT NULL,
    
    -- 대표자주민등록번호 (유니크)
    representative_resident_number VARCHAR(13) UNIQUE,
    
    -- 업태
    business_type VARCHAR(100),
    
    -- 종목
    business_category VARCHAR(100),
    
    -- 주소
    address TEXT,
    
    -- 전화번호
    phone_number VARCHAR(20),
    
    -- 이메일
    email VARCHAR(255),
    
    -- 생성 시간 (기본값: 현재 시간)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 최종 수정 시간 (기본값: 현재 시간)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
-- 사업자명으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_business_info_business_name 
ON business_info(business_name);

-- 대표자명으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_business_info_representative_name 
ON business_info(representative_name);

-- 업태로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_business_info_business_type 
ON business_info(business_type);

-- 생성 시간으로 정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_business_info_created_at 
ON business_info(created_at);

-- 트리거 생성: updated_at 자동 업데이트
CREATE TRIGGER IF NOT EXISTS update_business_info_updated_at
    AFTER UPDATE ON business_info
    FOR EACH ROW
    WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE business_info 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE business_registration_number = NEW.business_registration_number;
END;

-- 테이블 코멘트 (SQLite는 코멘트를 직접 지원하지 않으므로 별도 문서로 관리)
-- 테이블명: business_info
-- 설명: 개인 사업자의 기본 정보를 저장하는 테이블
-- 생성일: 2025-01-27
-- 작성자: VAT FileMaker Team
