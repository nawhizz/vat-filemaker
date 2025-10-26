"""
사업장정보 Repository

사업장정보 테이블에 대한 CRUD 작업을 담당합니다.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.schema import BusinessInfo


class BusinessInfoRepository:
    """
    사업장정보 Repository 클래스
    
    사업장정보 테이블에 대한 모든 데이터 접근 작업을 담당합니다.
    """
    
    def __init__(self, session: Session):
        """
        Repository 초기화
        
        Args:
            session: SQLAlchemy 세션 객체
        """
        self.session = session
    
    def create(self, business_data: Dict[str, Any]) -> BusinessInfo:
        """
        새로운 사업장정보 생성
        
        Args:
            business_data: 사업장정보 데이터 딕셔너리
            
        Returns:
            생성된 BusinessInfo 객체
            
        Raises:
            IntegrityError: 중복된 사업자등록번호 또는 주민등록번호
        """
        try:
            business_info = BusinessInfo.from_dict(business_data)
            self.session.add(business_info)
            self.session.commit()
            self.session.refresh(business_info)
            return business_info
        except IntegrityError as e:
            self.session.rollback()
            raise e
    
    def get_by_registration_number(self, registration_number: str) -> Optional[BusinessInfo]:
        """
        사업자등록번호로 사업장정보 조회
        
        Args:
            registration_number: 사업자등록번호
            
        Returns:
            BusinessInfo 객체 또는 None
        """
        return self.session.query(BusinessInfo).filter(
            BusinessInfo.business_registration_number == registration_number
        ).first()
    
    def get_by_resident_number(self, resident_number: str) -> Optional[BusinessInfo]:
        """
        대표자주민등록번호로 사업장정보 조회
        
        Args:
            resident_number: 대표자주민등록번호
            
        Returns:
            BusinessInfo 객체 또는 None
        """
        return self.session.query(BusinessInfo).filter(
            BusinessInfo.representative_resident_number == resident_number
        ).first()
    
    def get_by_business_name(self, business_name: str) -> List[BusinessInfo]:
        """
        사업자명으로 사업장정보 조회 (부분 일치)
        
        Args:
            business_name: 사업자명 (부분 일치)
            
        Returns:
            BusinessInfo 객체 리스트
        """
        return self.session.query(BusinessInfo).filter(
            BusinessInfo.business_name.like(f"%{business_name}%")
        ).all()
    
    def get_by_representative_name(self, representative_name: str) -> List[BusinessInfo]:
        """
        대표자명으로 사업장정보 조회 (부분 일치)
        
        Args:
            representative_name: 대표자명 (부분 일치)
            
        Returns:
            BusinessInfo 객체 리스트
        """
        return self.session.query(BusinessInfo).filter(
            BusinessInfo.representative_name.like(f"%{representative_name}%")
        ).all()
    
    def get_by_business_type(self, business_type: str) -> List[BusinessInfo]:
        """
        업태로 사업장정보 조회
        
        Args:
            business_type: 업태
            
        Returns:
            BusinessInfo 객체 리스트
        """
        return self.session.query(BusinessInfo).filter(
            BusinessInfo.business_type == business_type
        ).all()
    
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[BusinessInfo]:
        """
        모든 사업장정보 조회
        
        Args:
            limit: 조회할 최대 개수
            offset: 조회 시작 위치
            
        Returns:
            BusinessInfo 객체 리스트
        """
        query = self.session.query(BusinessInfo).offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update(self, registration_number: str, update_data: Dict[str, Any]) -> Optional[BusinessInfo]:
        """
        사업장정보 수정
        
        Args:
            registration_number: 사업자등록번호
            update_data: 수정할 데이터 딕셔너리
            
        Returns:
            수정된 BusinessInfo 객체 또는 None
            
        Raises:
            IntegrityError: 중복된 주민등록번호
        """
        try:
            business_info = self.get_by_registration_number(registration_number)
            if not business_info:
                return None
            
            # 업데이트할 필드만 수정
            for key, value in update_data.items():
                if hasattr(business_info, key) and value is not None:
                    setattr(business_info, key, value)
            
            self.session.commit()
            self.session.refresh(business_info)
            return business_info
        except IntegrityError as e:
            self.session.rollback()
            raise e
    
    def delete(self, registration_number: str) -> bool:
        """
        사업장정보 삭제
        
        Args:
            registration_number: 사업자등록번호
            
        Returns:
            삭제 성공 여부
        """
        business_info = self.get_by_registration_number(registration_number)
        if not business_info:
            return False
        
        self.session.delete(business_info)
        self.session.commit()
        return True
    
    def exists(self, registration_number: str) -> bool:
        """
        사업자등록번호 존재 여부 확인
        
        Args:
            registration_number: 사업자등록번호
            
        Returns:
            존재 여부
        """
        return self.session.query(BusinessInfo).filter(
            BusinessInfo.business_registration_number == registration_number
        ).first() is not None
    
    def count(self) -> int:
        """
        전체 사업장정보 개수 조회
        
        Returns:
            전체 개수
        """
        return self.session.query(BusinessInfo).count()
    
    def search(self, search_term: str) -> List[BusinessInfo]:
        """
        통합 검색 (사업자명, 대표자명, 업태, 종목에서 검색)
        
        Args:
            search_term: 검색어
            
        Returns:
            검색된 BusinessInfo 객체 리스트
        """
        return self.session.query(BusinessInfo).filter(
            BusinessInfo.business_name.like(f"%{search_term}%") |
            BusinessInfo.representative_name.like(f"%{search_term}%") |
            BusinessInfo.business_type.like(f"%{search_term}%") |
            BusinessInfo.business_category.like(f"%{search_term}%")
        ).all()
