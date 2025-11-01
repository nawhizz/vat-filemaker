-- 카드사 정보 테이블 생성 스크립트
-- SQLite 데이터베이스용 DDL

-- 카드사 정보 테이블 생성
CREATE TABLE IF NOT EXISTS card_company_info (
    -- 기본 키 (자동 증가)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 카드사 코드 (필수, 3바이트)
    card_company_code VARCHAR(3) NOT NULL,
    
    -- 카드사 한글명 (필수)
    card_company_name VARCHAR(255) NOT NULL,
    
    -- 카드사 영문명 (선택)
    card_company_name_en VARCHAR(255),
    
    -- 생성 시간 (기본값: 현재 시간)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 최종 수정 시간 (기본값: 현재 시간)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
-- 카드사 코드로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_company_info_card_company_code 
ON card_company_info(card_company_code);

-- 카드사 한글명으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_company_info_card_company_name 
ON card_company_info(card_company_name);

-- 카드사 영문명으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_company_info_card_company_name_en 
ON card_company_info(card_company_name_en);

-- 생성 시간으로 정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_company_info_created_at 
ON card_company_info(created_at);

-- 트리거 생성: updated_at 자동 업데이트
CREATE TRIGGER IF NOT EXISTS update_card_company_info_updated_at
    AFTER UPDATE ON card_company_info
    FOR EACH ROW
    WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE card_company_info 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

-- 테이블 코멘트 (SQLite는 코멘트를 직접 지원하지 않으므로 별도 문서로 관리)
-- 테이블명: card_company_info
-- 설명: 카드사 메타 정보를 저장하는 테이블 (business_number 컬럼 제거됨)
-- 수정일: 2025-11-01
-- 작성자: VAT FileMaker Team

