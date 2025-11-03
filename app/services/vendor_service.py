"""
거래처정보 서비스

거래처정보 관련 비즈니스 로직을 처리합니다.
"""

from typing import Optional, Dict, Any, List
from app.repositories.database import DatabaseInitializer
from app.repositories.vendor_repository import VendorRepository
from app.repositories.schema import VendorInfo
from app.config.settings import settings


class VendorService:
    """
    거래처정보 서비스 클래스
    
    거래처정보 관련 비즈니스 로직을 담당합니다.
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
        self.repository: Optional[VendorRepository] = None
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
            self.repository = VendorRepository(session)
            
        except Exception as e:
            raise RuntimeError(f"데이터베이스 초기화 실패: {e}")
    
    def _get_code_name(self, code_group: str, code: Optional[str]) -> Optional[str]:
        """
        공통코드에서 코드명 가져오기
        
        Args:
            code_group: 코드 그룹명
            code: 코드 값
        
        Returns:
            코드명 또는 None
        """
        if not code:
            return None
        
        try:
            from app.services.common_code_service import CommonCodeService
            common_code_service = CommonCodeService()
            # code_group을 소문자로 변환하여 조회
            common_code = common_code_service.get_common_code(code_group.lower(), code)
            return common_code.get('code_name') if common_code else None
        except:
            return None
    
    def create_vendor(self, data: Dict[str, Any]) -> VendorInfo:
        """
        새로운 거래처 정보 생성
        
        Args:
            data: 거래처 정보 데이터
        
        Returns:
            생성된 VendorInfo 객체
        
        Raises:
            ValueError: 필수 필드가 누락된 경우
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        # 필수 필드 검사
        required_fields = ['business_number', 'vendor_name']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field}은(는) 필수 입력 항목입니다.")
        
        try:
            return self.repository.create(data)
        except ValueError as e:
            # 제약조건 위반 등의 ValueError는 그대로 전달
            raise e
        except Exception as e:
            raise RuntimeError(f"거래처 정보 생성 실패: {e}")
    
    def get_vendor(self, vendor_id: int) -> Optional[Dict[str, Any]]:
        """
        거래처 정보 조회
        
        Args:
            vendor_id: 거래처 정보 ID
        
        Returns:
            거래처 정보 딕셔너리 또는 None (tax_type_name, business_status_name 포함)
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        vendor = self.repository.get(vendor_id)
        if not vendor:
            return None
        
        vendor_dict = vendor.to_dict()
        
        # 코드명 추가 (code_group을 소문자로 변환)
        vendor_dict['tax_type_name'] = self._get_code_name('tax_type', vendor.tax_type)
        vendor_dict['business_status_name'] = self._get_code_name('business_status', vendor.business_status)
        
        return vendor_dict
    
    def update_vendor(self, vendor_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        거래처 정보 수정
        
        Args:
            vendor_id: 거래처 정보 ID
            update_data: 수정할 데이터
        
        Returns:
            수정된 거래처 정보 딕셔너리 또는 None (tax_type_name, business_status_name 포함)
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            updated_vendor = self.repository.update(vendor_id, update_data)
            if not updated_vendor:
                return None
            
            vendor_dict = updated_vendor.to_dict()
            
            # 코드명 추가 (code_group을 소문자로 변환)
            vendor_dict['tax_type_name'] = self._get_code_name('tax_type', updated_vendor.tax_type)
            vendor_dict['business_status_name'] = self._get_code_name('business_status', updated_vendor.business_status)
            
            return vendor_dict
        except Exception as e:
            raise RuntimeError(f"거래처 정보 수정 실패: {e}")
    
    def delete_vendor(self, vendor_id: int) -> bool:
        """
        거래처 정보 삭제
        
        Args:
            vendor_id: 거래처 정보 ID
        
        Returns:
            삭제 성공 여부
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            return self.repository.delete(vendor_id)
        except Exception as e:
            raise RuntimeError(f"거래처 정보 삭제 실패: {e}")
    
    def get_all_vendors(self) -> List[Dict[str, Any]]:
        """
        모든 거래처 정보 목록 조회
        
        Returns:
            거래처 정보 리스트 (tax_type_name, business_status_name 포함)
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            from app.repositories.schema import VendorInfo
            session = self.db_initializer.get_session()
            results = session.query(VendorInfo).all()
            
            vendors = []
            for vendor in results:
                vendor_dict = vendor.to_dict()
                # 코드명 추가 (code_group을 소문자로 변환)
                vendor_dict['tax_type_name'] = self._get_code_name('tax_type', vendor.tax_type)
                vendor_dict['business_status_name'] = self._get_code_name('business_status', vendor.business_status)
                vendors.append(vendor_dict)
            
            return vendors
        except Exception as e:
            raise RuntimeError(f"거래처 정보 조회 실패: {e}")
    
    def search_vendors(
        self,
        business_number: Optional[str] = None,
        vendor_name: Optional[str] = None,
        tax_type: Optional[str] = None,
        business_status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        거래처 정보 검색
        
        Args:
            business_number: 사업자등록번호 (선택, 부분 일치)
            vendor_name: 거래처명 (선택, 부분 일치)
            tax_type: 과세유형 (선택)
            business_status: 사업자 상태 (선택)
        
        Returns:
            검색된 거래처 정보 리스트 (tax_type_name, business_status_name 포함)
        """
        if not self.repository:
            raise RuntimeError("Repository가 초기화되지 않았습니다.")
        
        try:
            from app.repositories.schema import VendorInfo
            
            session = self.db_initializer.get_session()
            query = session.query(VendorInfo)
            
            # 사업자등록번호로 검색 (부분 일치)
            if business_number:
                query = query.filter(VendorInfo.business_number.like(f"%{business_number}%"))
            
            # 거래처명으로 검색 (부분 일치)
            if vendor_name:
                query = query.filter(VendorInfo.vendor_name.like(f"%{vendor_name}%"))
            
            # 과세유형으로 필터링
            if tax_type:
                query = query.filter(VendorInfo.tax_type == tax_type)
            
            # 사업자 상태로 필터링
            if business_status:
                query = query.filter(VendorInfo.business_status == business_status)
            
            results = query.all()
            
            vendors = []
            for vendor in results:
                vendor_dict = vendor.to_dict()
                # 코드명 추가 (code_group을 소문자로 변환)
                vendor_dict['tax_type_name'] = self._get_code_name('tax_type', vendor.tax_type)
                vendor_dict['business_status_name'] = self._get_code_name('business_status', vendor.business_status)
                vendors.append(vendor_dict)
            
            return vendors
        except Exception as e:
            raise RuntimeError(f"거래처 정보 검색 실패: {e}")

