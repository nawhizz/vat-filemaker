"""
사업장 정보 서비스

사업장 정보 관련 비즈니스 로직을 처리합니다.
"""

from typing import Optional, Dict, Any, List
from app.repositories.database import DatabaseInitializer
from app.repositories.business_info_repository import BusinessInfoRepository
from app.repositories.schema import BusinessInfo


class BusinessService:
    """
    사업장 정보 서비스 클래스
    
    사업장 정보 관련 비즈니스 로직을 담당합니다.
    """
    
    def __init__(self, database_path: str = "data/vat_filemaker.db"):
        """
        서비스 초기화
        
        Args:
            database_path: 데이터베이스 파일 경로
        """
        self.db_initializer = DatabaseInitializer(database_path)
        self.repository: Optional[BusinessInfoRepository] = None
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
            self.repository = BusinessInfoRepository(session)
            
        except Exception as e:
            raise RuntimeError(f"데이터베이스 초기화 실패: {e}")
    
    def create_business_info(self, business_data: Dict[str, Any]) -> BusinessInfo:
        """
        새로운 사업장 정보 생성
        
        Args:
            business_data: 사업장 정보 데이터
            
        Returns:
            생성된 BusinessInfo 객체
            
        Raises:
            ValueError: 필수 필드가 누락된 경우
            IntegrityError: 중복된 사업자등록번호 또는 주민등록번호
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        # 필수 필드 검사
        required_fields = ['business_number', 'business_name', 'owner_name']
        for field in required_fields:
            if not business_data.get(field):
                raise ValueError(f"{field}은(는) 필수 입력 항목입니다.")
        
        # 사업자등록번호 중복 검사
        if self.repository.exists(business_data['business_number']):
            raise ValueError("이미 등록된 사업자등록번호입니다.")
        
        # 주민등록번호 중복 검사 (입력된 경우)
        resident_number = business_data.get('owner_resident_number')
        if resident_number and self.repository.get_by_resident_number(resident_number):
            raise ValueError("이미 등록된 주민등록번호입니다.")
        
        try:
            return self.repository.create(business_data)
        except Exception as e:
            raise RuntimeError(f"사업장 정보 생성 실패: {e}")
    
    def get_business_info(self, business_number: str) -> Optional[Dict[str, Any]]:
        """
        사업장 정보 조회
        
        Args:
            business_number: 사업자등록번호
            
        Returns:
            사업장 정보 딕셔너리 또는 None
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        business_info = self.repository.get_by_registration_number(business_number)
        return business_info.to_dict() if business_info else None
    
    def update_business_info(self, business_number: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        사업장 정보 수정
        
        Args:
            business_number: 사업자등록번호
            update_data: 수정할 데이터
            
        Returns:
            수정된 사업장 정보 딕셔너리 또는 None
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        # 주민등록번호 중복 검사 (변경된 경우)
        resident_number = update_data.get('owner_resident_number')
        if resident_number:
            existing = self.repository.get_by_resident_number(resident_number)
            if existing and existing.business_number != business_number:
                raise ValueError("이미 등록된 주민등록번호입니다.")
        
        try:
            updated_business = self.repository.update(business_number, update_data)
            return updated_business.to_dict() if updated_business else None
        except Exception as e:
            raise RuntimeError(f"사업장 정보 수정 실패: {e}")
    
    def delete_business_info(self, business_number: str) -> bool:
        """
        사업장 정보 삭제
        
        Args:
            business_number: 사업자등록번호
            
        Returns:
            삭제 성공 여부
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            return self.repository.delete(business_number)
        except Exception as e:
            raise RuntimeError(f"사업장 정보 삭제 실패: {e}")
    
    def search_business_info(self, search_term: str) -> List[Dict[str, Any]]:
        """
        사업장 정보 검색
        
        Args:
            search_term: 검색어
            
        Returns:
            검색된 사업장 정보 리스트
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            results = self.repository.search(search_term)
            return [business.to_dict() for business in results]
        except Exception as e:
            raise RuntimeError(f"사업장 정보 검색 실패: {e}")
    
    def get_all_business_info(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        모든 사업장 정보 조회
        
        Args:
            limit: 조회할 최대 개수
            offset: 조회 시작 위치
            
        Returns:
            사업장 정보 리스트
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            results = self.repository.get_all(limit, offset)
            return [business.to_dict() for business in results]
        except Exception as e:
            raise RuntimeError(f"사업장 정보 조회 실패: {e}")
    
    def get_business_count(self) -> int:
        """
        전체 사업장 정보 개수 조회
        
        Returns:
            전체 개수
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            return self.repository.count()
        except Exception as e:
            raise RuntimeError(f"사업장 정보 개수 조회 실패: {e}")
    
    def validate_business_number(self, business_number: str) -> bool:
        """
        사업자등록번호 유효성 검사
        
        Args:
            business_number: 사업자등록번호
            
        Returns:
            유효성 검사 결과
        """
        # 하이픈 제거
        clean_number = business_number.replace('-', '')
        
        # 10자리 숫자인지 확인
        if not clean_number.isdigit() or len(clean_number) != 10:
            return False
        
        # 사업자등록번호 체크섬 검증 (간단한 버전)
        # 실제로는 더 복잡한 검증 로직이 필요할 수 있음
        return True
    
    def format_business_number(self, business_number: str) -> str:
        """
        사업자등록번호 포맷팅
        
        Args:
            business_number: 사업자등록번호
            
        Returns:
            포맷팅된 사업자등록번호
        """
        # 하이픈 제거
        clean_number = business_number.replace('-', '')
        
        # 10자리 숫자인지 확인
        if len(clean_number) != 10 or not clean_number.isdigit():
            return business_number
        
        # XXX-XX-XXXXX 형식으로 포맷팅
        return f"{clean_number[:3]}-{clean_number[3:5]}-{clean_number[5:]}"
