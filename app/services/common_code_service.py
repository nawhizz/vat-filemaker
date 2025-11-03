"""
공통코드 서비스

공통코드 관련 비즈니스 로직을 처리합니다.
"""

from typing import Optional, Dict, Any, List
from app.repositories.database import DatabaseInitializer
from app.repositories.common_code_repository import CommonCodeRepository
from app.repositories.schema import CommonCode
from app.config.settings import settings


class CommonCodeService:
    """
    공통코드 서비스 클래스
    
    공통코드 관련 비즈니스 로직을 담당합니다.
    """
    
    def __init__(self, database_path: Optional[str] = None):
        """
        서비스 초기화
        
        Args:
            database_path: 데이터베이스 파일 경로 (None인 경우 설정에서 가져옴)
        """
        if database_path is None:
            database_path = settings.get_database_path()
        self.db_initializer = DatabaseInitializer(database_path)
        self.repository: Optional[CommonCodeRepository] = None
        self._initialize_repository()
    
    def _initialize_repository(self) -> None:
        """
        Repository 초기화
        
        데이터베이스가 초기화되지 않은 경우 초기화하고 Repository를 생성합니다.
        """
        try:
            # 데이터베이스 초기화 (이미 초기화된 경우 무시됨)
            self.db_initializer.initialize_database()
            
            # 세션 생성
            session = self.db_initializer.get_session()
            self.repository = CommonCodeRepository(session)
            
        except Exception as e:
            raise RuntimeError(f"데이터베이스 초기화 실패: {e}")
    
    def create_common_code(self, data: Dict[str, Any]) -> CommonCode:
        """
        새로운 공통코드 생성
        
        Args:
            data: 공통코드 데이터
        
        Returns:
            생성된 CommonCode 객체
        
        Raises:
            ValueError: 필수 필드가 누락된 경우
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        # 필수 필드 검사
        required_fields = ['code_group', 'code', 'code_name', 'code_abbr']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field}은(는) 필수 입력 항목입니다.")
        
        try:
            return self.repository.create(data)
        except ValueError as e:
            # 제약조건 위반 등의 ValueError는 그대로 전달
            raise e
        except Exception as e:
            raise RuntimeError(f"공통 코드 생성 실패: {e}")
    
    def get_common_code(self, code_group: str, code: str) -> Optional[Dict[str, Any]]:
        """
        공통코드 조회
        
        Args:
            code_group: 코드 그룹명
            code: 코드 값
        
        Returns:
            공통코드 딕셔너리 또는 None
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        common_code = self.repository.get(code_group, code)
        return common_code.to_dict() if common_code else None
    
    def update_common_code(
        self, 
        code_group: str, 
        code: str, 
        update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        공통코드 수정
        
        Args:
            code_group: 코드 그룹명
            code: 코드 값
            update_data: 수정할 데이터
        
        Returns:
            수정된 공통코드 딕셔너리 또는 None
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            updated_common_code = self.repository.update(code_group, code, update_data)
            return updated_common_code.to_dict() if updated_common_code else None
        except Exception as e:
            raise RuntimeError(f"공통 코드 수정 실패: {e}")
    
    def delete_common_code(self, code_group: str, code: str) -> bool:
        """
        공통코드 삭제
        
        Args:
            code_group: 코드 그룹명
            code: 코드 값
        
        Returns:
            삭제 성공 여부
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            return self.repository.delete(code_group, code)
        except Exception as e:
            raise RuntimeError(f"공통 코드 삭제 실패: {e}")
    
    def get_all_common_codes(self) -> List[Dict[str, Any]]:
        """
        모든 공통코드 목록 조회
        
        Returns:
            공통코드 리스트
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            from app.repositories.schema import CommonCode
            session = self.db_initializer.get_session()
            results = session.query(CommonCode).order_by(
                CommonCode.code_group, CommonCode.sort_order
            ).all()
            return [common_code.to_dict() for common_code in results]
        except Exception as e:
            raise RuntimeError(f"공통 코드 조회 실패: {e}")
    
    def get_common_codes_by_group(self, code_group: str) -> List[Dict[str, Any]]:
        """
        코드 그룹별 공통코드 목록 조회
        
        Args:
            code_group: 코드 그룹명
        
        Returns:
            공통코드 리스트
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            codes = self.repository.get_by_group(code_group)
            return [common_code.to_dict() for common_code in codes]
        except Exception as e:
            raise RuntimeError(f"공통 코드 조회 실패: {e}")
    
    def search_common_codes(
        self,
        code_group: Optional[str] = None,
        code: Optional[str] = None,
        code_name: Optional[str] = None,
        code_abbr: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        공통코드 검색
        
        Args:
            code_group: 코드 그룹명 (선택, 부분 일치)
            code: 코드 값 (선택, 부분 일치)
            code_name: 코드명 (선택, 부분 일치)
            code_abbr: 코드약어명 (선택, 부분 일치)
            is_active: 사용 여부 (선택)
        
        Returns:
            검색된 공통코드 리스트
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            from sqlalchemy import or_
            from app.repositories.schema import CommonCode
            
            session = self.db_initializer.get_session()
            query = session.query(CommonCode)
            
            # 코드 그룹으로 검색 (부분 일치)
            if code_group:
                query = query.filter(CommonCode.code_group.like(f"%{code_group}%"))
            
            # 코드로 검색 (부분 일치)
            if code:
                query = query.filter(CommonCode.code.like(f"%{code}%"))
            
            # 코드명으로 검색 (부분 일치)
            if code_name:
                query = query.filter(CommonCode.code_name.like(f"%{code_name}%"))
            
            # 코드약어명으로 검색 (부분 일치)
            if code_abbr:
                query = query.filter(CommonCode.code_abbr.like(f"%{code_abbr}%"))
            
            # 사용 여부로 필터링
            if is_active is not None:
                query = query.filter(CommonCode.is_active == is_active)
            
            # 정렬: 코드 그룹, 정렬 순서
            results = query.order_by(CommonCode.code_group, CommonCode.sort_order).all()
            return [common_code.to_dict() for common_code in results]
        except Exception as e:
            raise RuntimeError(f"공통 코드 검색 실패: {e}")

