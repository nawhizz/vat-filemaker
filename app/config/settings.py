"""
설정 관리 모듈

python-dotenv를 사용하여 .env 파일에서 환경 변수를 로드하고 관리합니다.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


# 프로젝트 루트 디렉토리 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# .env 파일 로드 (프로젝트 루트에서)
load_dotenv(dotenv_path=ENV_FILE)


class Settings:
    """
    설정 클래스
    
    .env 파일에서 환경 변수를 로드하고 애플리케이션 설정을 관리합니다.
    """
    
    # 데이터베이스 설정
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "data/vat_filemaker.db")
    
    # 로깅 설정
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # 국세청 API 설정 (향후 구현)
    NTS_API_KEY: Optional[str] = os.getenv("NTS_API_KEY", None)
    NTS_API_URL: str = os.getenv("NTS_API_URL", "https://openapi.nts.go.kr")
    
    # UI 설정
    UI_THEME: str = os.getenv("UI_THEME", "Fluent")
    
    # 개발 모드 설정
    DEV_MODE: bool = os.getenv("DEV_MODE", "False").lower() == "true"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # 암호화 설정
    ENCRYPTION_KEY: Optional[str] = os.getenv("ENCRYPTION_KEY", None)
    
    @classmethod
    def get_database_path(cls) -> str:
        """
        데이터베이스 파일 경로 반환
        
        Returns:
            데이터베이스 파일 경로
        """
        db_path = Path(cls.DATABASE_PATH)
        # 상대 경로인 경우 프로젝트 루트 기준으로 절대 경로 변환
        if not db_path.is_absolute():
            return str(PROJECT_ROOT / db_path)
        return str(db_path)
    
    @classmethod
    def get_log_file_path(cls) -> str:
        """
        로그 파일 경로 반환
        
        Returns:
            로그 파일 경로
        """
        log_path = Path(cls.LOG_FILE)
        # 상대 경로인 경우 프로젝트 루트 기준으로 절대 경로 변환
        if not log_path.is_absolute():
            return str(PROJECT_ROOT / log_path)
        return str(log_path)


# 전역 설정 객체
settings = Settings()

