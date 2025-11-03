-- 거래처정보 테이블 생성 스크립트
-- SQLite 데이터베이스용 DDL

-- 거래처정보 테이블 생성
CREATE TABLE IF NOT EXISTS vendor_info (
    -- 기본 키 (자동 증가)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 거래처 사업자등록번호 (유니크)
    business_number VARCHAR(10) UNIQUE NOT NULL,
    
    -- 거래처명
    vendor_name VARCHAR(255) NOT NULL,
    
    -- 과세유형 (01:일반과세자, 02:간이과세자, 03:과세특례자, 04:면세사업자 등등)
    tax_type VARCHAR(10),
    
    -- 사업자 상태 (01:계속사업자, 02:휴업, 03:폐업 등)
    business_status VARCHAR(10),
    
    -- 상태 업데이트 날짜
    status_updated_at DATETIME,
    
    -- 생성 시간 (기본값: 현재 시간)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 최종 수정 시간 (기본값: 현재 시간)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
-- 사업자등록번호로 검색할 때 성능 향상을 위한 인덱스 (UNIQUE 제약조건으로 이미 인덱스 생성됨, 하지만 명시적으로 추가)
CREATE INDEX IF NOT EXISTS idx_vendor_info_business_number 
ON vendor_info(business_number);

-- 거래처명으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_vendor_info_vendor_name 
ON vendor_info(vendor_name);

-- 과세유형으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_vendor_info_tax_type 
ON vendor_info(tax_type);

-- 사업자 상태로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_vendor_info_business_status 
ON vendor_info(business_status);

-- 상태 업데이트 날짜로 정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_vendor_info_status_updated_at 
ON vendor_info(status_updated_at);

-- 생성 시간으로 정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_vendor_info_created_at 
ON vendor_info(created_at);

-- 복합 인덱스: 과세유형과 사업자 상태 조합 검색 성능 향상
CREATE INDEX IF NOT EXISTS idx_vendor_info_tax_status 
ON vendor_info(tax_type, business_status);

-- 트리거 생성: updated_at 자동 업데이트
CREATE TRIGGER IF NOT EXISTS update_vendor_info_updated_at
    AFTER UPDATE ON vendor_info
    FOR EACH ROW
    WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE vendor_info 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

-- 테이블 코멘트 (SQLite는 코멘트를 직접 지원하지 않으므로 별도 문서로 관리)
-- 테이블명: vendor_info
-- 설명: 거래처 정보를 저장하는 테이블 (사업자등록번호, 과세유형, 사업자 상태 등)
-- 생성일: 2025-01-27
-- 작성자: VAT FileMaker Team

