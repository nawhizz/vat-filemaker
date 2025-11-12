-- 카드사용내역 테이블 생성 스크립트
-- SQLite 데이터베이스용 DDL

-- 카드사용내역 테이블 생성
CREATE TABLE IF NOT EXISTS card_transaction (
    -- 기본 키 (자동 증가)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 참조: 카드사 ID (FK -> card_company_info.id)
    card_company_id INTEGER NOT NULL,
    
    -- 거래 일자
    transaction_date DATETIME NOT NULL,
    
    -- 카드번호(마스킹)
    masked_card_number VARCHAR(50),
    
    -- 거래취소여부 (Boolean: FALSE/0 = 정상거래, TRUE/1 = 취소거래)
    -- SQLite는 BOOLEAN을 직접 지원하지 않으므로 내부적으로 INTEGER로 저장됨
    is_cancel BOOLEAN DEFAULT FALSE,
    
    -- 거래 금액 (DECIMAL -> NUMERIC 사용)
    amount NUMERIC(15, 2) NOT NULL,
    
    -- 거래처명
    vendor_name VARCHAR(255),
    
    -- 사업자등록번호
    business_number VARCHAR(10),
    
    -- 승인번호
    approval_number VARCHAR(20),
    
    -- 참조: 카드 ID (FK -> card_info.id)
    card_id INTEGER,
    
    -- 참조: 거래처 ID (FK -> vendor_info.id)
    vendor_id INTEGER,
    
    -- 생성 시간 (기본값: 현재 시간)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 최종 수정 시간 (기본값: 현재 시간)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 외래 키 제약조건
    FOREIGN KEY (card_company_id) 
        REFERENCES card_company_info(id) 
        ON DELETE RESTRICT,
    
    FOREIGN KEY (card_id) 
        REFERENCES card_info(id) 
        ON DELETE SET NULL,
    
    FOREIGN KEY (vendor_id) 
        REFERENCES vendor_info(id) 
        ON DELETE SET NULL
);

-- 인덱스 생성
-- 카드사 ID로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_transaction_card_company_id 
ON card_transaction(card_company_id);

-- 거래 일자로 검색/정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_transaction_transaction_date 
ON card_transaction(transaction_date);

-- 거래취소여부로 필터링할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_transaction_is_cancel 
ON card_transaction(is_cancel);

-- 카드 ID로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_transaction_card_id 
ON card_transaction(card_id);

-- 거래처 ID로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_transaction_vendor_id 
ON card_transaction(vendor_id);

-- 사업자등록번호로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_transaction_business_number 
ON card_transaction(business_number);

-- 승인번호로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_transaction_approval_number 
ON card_transaction(approval_number);

-- 생성 시간으로 정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_card_transaction_created_at 
ON card_transaction(created_at);

-- 복합 인덱스: 거래 일자와 거래취소여부 조합 검색 성능 향상
CREATE INDEX IF NOT EXISTS idx_card_transaction_date_cancel 
ON card_transaction(transaction_date, is_cancel);

-- 복합 인덱스: 카드사 ID와 거래 일자 조합 검색 성능 향상
CREATE INDEX IF NOT EXISTS idx_card_transaction_company_date 
ON card_transaction(card_company_id, transaction_date);

-- 복합 인덱스: 카드 ID와 거래 일자 조합 검색 성능 향상
CREATE INDEX IF NOT EXISTS idx_card_transaction_card_date 
ON card_transaction(card_id, transaction_date);

-- 트리거 생성: updated_at 자동 업데이트
CREATE TRIGGER IF NOT EXISTS update_card_transaction_updated_at
    AFTER UPDATE ON card_transaction
    FOR EACH ROW
    WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE card_transaction 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

-- 테이블 코멘트 (SQLite는 코멘트를 직접 지원하지 않으므로 별도 문서로 관리)
-- 테이블명: card_transaction
-- 설명: 카드사용내역을 저장하는 테이블 (거래 일자, 금액, 거래처 정보 등)
-- 생성일: 2025-01-27
-- 작성자: VAT FileMaker Team

