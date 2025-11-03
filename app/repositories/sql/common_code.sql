-- 공통 코드 테이블 생성 스크립트
-- SQLite 데이터베이스용 DDL

-- 공통 코드 테이블 생성
CREATE TABLE IF NOT EXISTS common_code (
    -- 코드 그룹명 (Primary Key - 복합 키의 첫 번째 컬럼)
    code_group VARCHAR(100) NOT NULL,
    
    -- 코드 값 (Primary Key - 복합 키의 두 번째 컬럼)
    code VARCHAR(100) NOT NULL,
    
    -- 코드명
    code_name VARCHAR(255) NOT NULL,

    -- 코드약어명
    code_abbr VARCHAR(255) NOT NULL,

    -- 정렬 순서
    sort_order INTEGER DEFAULT 0,
    
    -- 사용여부 (Boolean: FALSE/0 = 비활성, TRUE/1 = 활성)
    -- SQLite는 BOOLEAN을 직접 지원하지 않으므로 내부적으로 INTEGER로 저장됨
    is_active BOOLEAN DEFAULT TRUE,
    
    -- 비고
    description TEXT,
    
    -- 생성 시간 (기본값: 현재 시간)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 최종 수정 시간 (기본값: 현재 시간)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 복합 기본 키 (code_group, code)
    PRIMARY KEY (code_group, code)
);

-- 인덱스 생성
-- 코드 그룹으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_common_code_code_group 
ON common_code(code_group);

-- 코드로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_common_code_code 
ON common_code(code);

-- 코드명으로 검색할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_common_code_code_name 
ON common_code(code_name);

-- 사용여부로 필터링할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_common_code_is_active 
ON common_code(is_active);

-- 정렬 순서로 정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_common_code_sort_order 
ON common_code(sort_order);

-- 생성 시간으로 정렬할 때 성능 향상을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_common_code_created_at 
ON common_code(created_at);

-- 복합 인덱스: 코드 그룹과 사용여부 조합 검색 성능 향상
CREATE INDEX IF NOT EXISTS idx_common_code_group_active 
ON common_code(code_group, is_active);

-- 복합 인덱스: 코드 그룹과 정렬 순서 조합 검색 및 정렬 성능 향상
CREATE INDEX IF NOT EXISTS idx_common_code_group_sort 
ON common_code(code_group, sort_order);

-- 트리거 생성: updated_at 자동 업데이트
CREATE TRIGGER IF NOT EXISTS update_common_code_updated_at
    AFTER UPDATE ON common_code
    FOR EACH ROW
    WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE common_code 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE code_group = NEW.code_group AND code = NEW.code;
END;




-- 테이블 코멘트 (SQLite는 코멘트를 직접 지원하지 않으므로 별도 문서로 관리)
-- 테이블명: common_code
-- 설명: 공통 코드(코드 그룹별 코드 값)를 저장하는 테이블
-- 생성일: 2025-01-27
-- 작성자: VAT FileMaker Team

