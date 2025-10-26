"""
데이터베이스 초기화 스크립트

SQLite 데이터베이스를 초기화하고 테이블을 생성합니다.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.repositories.schema import Base, BusinessInfo


class DatabaseInitializer:
    """
    데이터베이스 초기화 클래스
    
    SQLite 데이터베이스 생성 및 테이블 초기화를 담당합니다.
    """
    
    def __init__(self, database_path: str = "data/vat_filemaker.db"):
        """
        데이터베이스 초기화자 생성
        
        Args:
            database_path: 데이터베이스 파일 경로
        """
        self.database_path = database_path
        self.engine = None
        self.SessionLocal = None
    
    def create_database_directory(self) -> None:
        """
        데이터베이스 디렉토리 생성
        
        데이터베이스 파일이 저장될 디렉토리를 생성합니다.
        """
        db_dir = Path(self.database_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def create_engine(self) -> None:
        """
        SQLAlchemy 엔진 생성
        
        SQLite 데이터베이스 연결 엔진을 생성합니다.
        """
        # 데이터베이스 디렉토리 생성
        self.create_database_directory()
        
        # SQLite 연결 문자열 생성
        database_url = f"sqlite:///{self.database_path}"
        
        # 엔진 생성 (에코 모드로 SQL 쿼리 로깅)
        self.engine = create_engine(
            database_url,
            echo=True,  # 개발 시에만 True, 운영에서는 False
            connect_args={"check_same_thread": False}  # SQLite 멀티스레드 지원
        )
        
        # 세션 팩토리 생성
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def create_tables(self) -> None:
        """
        모든 테이블 생성
        
        SQLAlchemy 모델을 기반으로 테이블을 생성합니다.
        """
        if not self.engine:
            raise RuntimeError("엔진이 초기화되지 않았습니다. create_engine()을 먼저 호출하세요.")
        
        # 모든 테이블 생성
        Base.metadata.create_all(bind=self.engine)
        print(f"테이블이 성공적으로 생성되었습니다: {self.database_path}")
    
    def execute_sql_file(self, sql_file_path: str) -> None:
        """
        SQL 파일 실행
        
        지정된 SQL 파일을 실행합니다.
        
        Args:
            sql_file_path: 실행할 SQL 파일 경로
        """
        if not self.engine:
            raise RuntimeError("엔진이 초기화되지 않았습니다. create_engine()을 먼저 호출하세요.")
        
        sql_file = Path(sql_file_path)
        if not sql_file.exists():
            raise FileNotFoundError(f"SQL 파일을 찾을 수 없습니다: {sql_file_path}")
        
        # SQL 파일 읽기
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # SQL 실행
        with self.engine.connect() as connection:
            # 트리거는 별도로 처리 (세미콜론 분리 시 문제 발생)
            if 'CREATE TRIGGER' in sql_content:
                # 트리거 부분을 별도로 추출
                trigger_start = sql_content.find('CREATE TRIGGER')
                if trigger_start != -1:
                    trigger_sql = sql_content[trigger_start:].strip()
                    connection.execute(text(trigger_sql))
            
            # 나머지 SQL 문장들 실행
            sql_without_trigger = sql_content[:sql_content.find('CREATE TRIGGER')] if 'CREATE TRIGGER' in sql_content else sql_content
            sql_statements = [stmt.strip() for stmt in sql_without_trigger.split(';') if stmt.strip()]
            
            for statement in sql_statements:
                if statement and not statement.startswith('--'):
                    connection.execute(text(statement))
            
            connection.commit()
        
        print(f"SQL 파일이 성공적으로 실행되었습니다: {sql_file_path}")
    
    def initialize_database(self) -> None:
        """
        데이터베이스 전체 초기화
        
        데이터베이스 생성부터 테이블 생성까지 모든 과정을 수행합니다.
        """
        try:
            print("데이터베이스 초기화를 시작합니다...")
            
            # 1. 엔진 생성
            self.create_engine()
            print("데이터베이스 엔진이 생성되었습니다.")
            
            # 2. 테이블 생성 (SQLAlchemy 모델 기반)
            self.create_tables()
            
            # 3. 추가 SQL 스크립트 실행 (인덱스, 트리거 등)
            sql_file_path = Path(__file__).parent / "sql" / "business_info.sql"
            if sql_file_path.exists():
                self.execute_sql_file(str(sql_file_path))
            
            print("데이터베이스 초기화가 완료되었습니다!")
            
        except Exception as e:
            print(f"데이터베이스 초기화 중 오류가 발생했습니다: {e}")
            raise
    
    def get_session(self):
        """
        데이터베이스 세션 반환
        
        Returns:
            SQLAlchemy 세션 객체
        """
        if not self.SessionLocal:
            raise RuntimeError("세션이 초기화되지 않았습니다. initialize_database()을 먼저 호출하세요.")
        
        return self.SessionLocal()


def initialize_database(database_path: str = "data/vat_filemaker.db") -> DatabaseInitializer:
    """
    데이터베이스 초기화 함수
    
    Args:
        database_path: 데이터베이스 파일 경로
        
    Returns:
        초기화된 DatabaseInitializer 인스턴스
    """
    initializer = DatabaseInitializer(database_path)
    initializer.initialize_database()
    return initializer


if __name__ == "__main__":
    # 스크립트 직접 실행 시 데이터베이스 초기화
    db_initializer = initialize_database()
    print("데이터베이스 초기화가 완료되었습니다.")
