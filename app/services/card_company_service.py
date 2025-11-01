"""
카드사 정보 서비스

카드사 정보 관련 비즈니스 로직을 처리합니다.
"""

from typing import Optional, Dict, Any, List
from app.repositories.database import DatabaseInitializer
from app.repositories.card_company_repository import CardCompanyRepository
from app.repositories.schema import CardCompanyInfo


class CardCompanyService:
  """
  카드사 정보 서비스 클래스
  
  카드사 정보 관련 비즈니스 로직을 담당합니다.
  """
  
  def __init__(self, database_path: str = "data/vat_filemaker.db"):
    """
    서비스 초기화
    
    Args:
      database_path: 데이터베이스 파일 경로
    """
    self.db_initializer = DatabaseInitializer(database_path)
    self.repository: Optional[CardCompanyRepository] = None
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
      self.repository = CardCompanyRepository(session)
      
    except Exception as e:
      raise RuntimeError(f"데이터베이스 초기화 실패: {e}")
  
  def create_card_company(self, data: Dict[str, Any]) -> CardCompanyInfo:
    """
    새로운 카드사 정보 생성
    
    Args:
      data: 카드사 정보 데이터
    
    Returns:
      생성된 CardCompanyInfo 객체
    
    Raises:
      ValueError: 필수 필드가 누락된 경우
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    # 필수 필드 검사
    required_fields = ['card_company_code', 'card_company_name']
    for field in required_fields:
      if not data.get(field):
        raise ValueError(f"{field}은(는) 필수 입력 항목입니다.")
    
    try:
      return self.repository.create(data)
    except ValueError as e:
      # 제약조건 위반 등의 ValueError는 그대로 전달
      raise e
    except Exception as e:
      raise RuntimeError(f"카드사 정보 생성 실패: {e}")
  
  def get_card_company(self, card_company_id: int) -> Optional[Dict[str, Any]]:
    """
    카드사 정보 조회
    
    Args:
      card_company_id: 카드사 정보 ID
    
    Returns:
      카드사 정보 딕셔너리 또는 None
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    card_company = self.repository.get(card_company_id)
    return card_company.to_dict() if card_company else None
  
  def update_card_company(self, card_company_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    카드사 정보 수정
    
    Args:
      card_company_id: 카드사 정보 ID
      update_data: 수정할 데이터
    
    Returns:
      수정된 카드사 정보 딕셔너리 또는 None
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      updated_card_company = self.repository.update(card_company_id, update_data)
      return updated_card_company.to_dict() if updated_card_company else None
    except Exception as e:
      raise RuntimeError(f"카드사 정보 수정 실패: {e}")
  
  def delete_card_company(self, card_company_id: int) -> bool:
    """
    카드사 정보 삭제
    
    Args:
      card_company_id: 카드사 정보 ID
    
    Returns:
      삭제 성공 여부
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      return self.repository.delete(card_company_id)
    except Exception as e:
      raise RuntimeError(f"카드사 정보 삭제 실패: {e}")
  
  def get_all_card_companies(self) -> List[Dict[str, Any]]:
    """
    모든 카드사 정보 목록 조회
    
    Returns:
      카드사 정보 리스트
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      from app.repositories.schema import CardCompanyInfo
      session = self.db_initializer.get_session()
      results = session.query(CardCompanyInfo).all()
      return [card_company.to_dict() for card_company in results]
    except Exception as e:
      raise RuntimeError(f"카드사 정보 조회 실패: {e}")
  
  def search_card_companies(
    self, 
    card_company_code: Optional[str] = None,
    card_company_name: Optional[str] = None
  ) -> List[Dict[str, Any]]:
    """
    카드사 정보 검색
    
    Args:
      card_company_code: 카드사 코드 (선택, 부분 일치)
      card_company_name: 카드사 명칭 (선택, 부분 일치)
    
    Returns:
      검색된 카드사 정보 리스트
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      from sqlalchemy import or_
      from app.repositories.schema import CardCompanyInfo
      
      session = self.db_initializer.get_session()
      query = session.query(CardCompanyInfo)
      
      # 카드사 코드로 검색 (부분 일치)
      if card_company_code:
        query = query.filter(CardCompanyInfo.card_company_code.like(f"%{card_company_code}%"))
      
      # 카드사 명칭으로 검색 (부분 일치)
      if card_company_name:
        query = query.filter(
          or_(
            CardCompanyInfo.card_company_name.like(f"%{card_company_name}%"),
            CardCompanyInfo.card_company_name_en.like(f"%{card_company_name}%")
          )
        )
      
      results = query.all()
      return [card_company.to_dict() for card_company in results]
    except Exception as e:
      raise RuntimeError(f"카드사 정보 검색 실패: {e}")

