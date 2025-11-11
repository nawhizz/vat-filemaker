-- 카드 정보 테이블 생성 스크립트
-- SQLite 데이터베이스용 DDL

-- 카드 정보 테이블 생성
CREATE TABLE IF NOT EXISTS card_info (
    -- 기본 키 (자동 증가)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 카드번호 (암호화된 값 저장)
    card_number VARCHAR(255) NOT NULL,
    
    -- 카드번호 (마스킹된 값 저장, 사용자 입력)
    masked_card_number VARCHAR(50),
    
    -- 카드명
    card_name VARCHAR(255) NOT NULL,
    
    -- 카드유형
    card_type VARCHAR(50),
    
    -- 참조: 카드사 ID (FK -> card_company_info.id)
    card_company_id INTEGER NOT NULL,
    
    -- 사용여부 (Boolean: FALSE/0 = 비활성, TRUE/1 = 활성)
    -- SQLite는 BOOLEAN을 직접 지원하지 않으므로 내부적으로 INTEGER로 저장됨
    is_active BOOLEAN DEFAULT TRUE,
    
    -- 생성 시간 (기본값: 현재 시간)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 최종 수정 시간 (기본값: 현재 시간)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 외래 키 제약조건
    FOREIGN KEY (card_company_id) 
        REFERENCES card_company_info(id) 
        ON DELETE RESTRICT
);

-- 인덱스 생성
-- 카드사 ID로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_info_card_company_id 
ON card_info(card_company_id);

-- 카드명으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_info_card_name 
ON card_info(card_name);

-- 카드유형으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_info_card_type 
ON card_info(card_type);

-- 사용여부로 필터링할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_info_is_active 
ON card_info(is_active);

-- 생성 시간으로 정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_info_created_at 
ON card_info(created_at);

-- 복합 인덱스: 카드사 ID와 사용여부 조합 검색 성능 향상
CREATE INDEX IF NOT EXISTS idx_card_info_company_active 
ON card_info(card_company_id, is_active);

-- 카드번호는 암호화되어 있지만, 중복 체크를 위한 인덱스 (선택적)
CREATE UNIQUE INDEX IF NOT EXISTS idx_card_info_card_number 
ON card_info(card_number);

-- 트리거 생성: updated_at 자동 업데이트
CREATE TRIGGER IF NOT EXISTS update_card_info_updated_at
    AFTER UPDATE ON card_info
    FOR EACH ROW
    WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE card_info 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

-- 테이블 코멘트 (SQLite는 코멘트를 직접 지원하지 않으므로 별도 문서로 관리)
-- 테이블명: card_info
-- 설명: 카드 정보를 저장하는 테이블 (카드번호는 암호화하여 저장)
-- 생성일: 2025-11-01
-- 작성자: VAT FileMaker Team

