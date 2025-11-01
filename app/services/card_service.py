"""
카드 정보 서비스

카드 정보 관련 비즈니스 로직을 처리합니다.
"""

from typing import Optional, Dict, Any, List
from app.repositories.database import DatabaseInitializer
from app.repositories.card_repository import CardRepository
from app.repositories.schema import CardInfo
from app.config.settings import settings


class CardService:
  """
  카드 정보 서비스 클래스
  
  카드 정보 관련 비즈니스 로직을 담당합니다.
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
    self.repository: Optional[CardRepository] = None
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
      self.repository = CardRepository(session)
      
    except Exception as e:
      raise RuntimeError(f"데이터베이스 초기화 실패: {e}")
  
  def create_card(self, data: Dict[str, Any]) -> CardInfo:
    """
    새로운 카드 정보 생성
    
    Args:
      data: 카드 정보 데이터
    
    Returns:
      생성된 CardInfo 객체
    
    Raises:
      ValueError: 필수 필드가 누락된 경우
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    # 필수 필드 검사
    required_fields = ['card_number', 'card_name', 'card_company_id']
    for field in required_fields:
      if not data.get(field):
        raise ValueError(f"{field}은(는) 필수 입력 항목입니다.")
    
    try:
      return self.repository.create(data)
    except ValueError as e:
      # 제약조건 위반 등의 ValueError는 그대로 전달
      raise e
    except Exception as e:
      raise RuntimeError(f"카드 정보 생성 실패: {e}")
  
  def get_card(self, card_id: int) -> Optional[Dict[str, Any]]:
    """
    카드 정보 조회
    
    Args:
      card_id: 카드 정보 ID
    
    Returns:
      카드 정보 딕셔너리 또는 None
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    card = self.repository.get(card_id)
    return card.to_dict() if card else None
  
  def update_card(self, card_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    카드 정보 수정
    
    Args:
      card_id: 카드 정보 ID
      update_data: 수정할 데이터
    
    Returns:
      수정된 카드 정보 딕셔너리 또는 None
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      updated_card = self.repository.update(card_id, update_data)
      return updated_card.to_dict() if updated_card else None
    except Exception as e:
      raise RuntimeError(f"카드 정보 수정 실패: {e}")
  
  def delete_card(self, card_id: int) -> bool:
    """
    카드 정보 삭제
    
    Args:
      card_id: 카드 정보 ID
    
    Returns:
      삭제 성공 여부
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      return self.repository.delete(card_id)
    except Exception as e:
      raise RuntimeError(f"카드 정보 삭제 실패: {e}")
  
  def get_all_cards(self) -> List[Dict[str, Any]]:
    """
    모든 카드 정보 목록 조회
    
    Returns:
      카드 정보 리스트
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      from app.repositories.schema import CardInfo
      session = self.db_initializer.get_session()
      results = session.query(CardInfo).all()
      return [card.to_dict() for card in results]
    except Exception as e:
      raise RuntimeError(f"카드 정보 조회 실패: {e}")
  
  def search_cards(
    self, 
    card_name: Optional[str] = None,
    card_type: Optional[str] = None,
    card_company_id: Optional[int] = None,
    is_active: Optional[bool] = None
  ) -> List[Dict[str, Any]]:
    """
    카드 정보 검색
    
    Args:
      card_name: 카드명 (선택, 부분 일치)
      card_type: 카드유형 (선택, 부분 일치)
      card_company_id: 카드사 ID (선택, 정확 일치)
      is_active: 사용여부 (선택, 정확 일치)
    
    Returns:
      검색된 카드 정보 리스트
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      from app.repositories.schema import CardInfo
      
      session = self.db_initializer.get_session()
      query = session.query(CardInfo)
      
      # 카드명으로 검색 (부분 일치)
      if card_name:
        query = query.filter(CardInfo.card_name.like(f"%{card_name}%"))
      
      # 카드유형으로 검색 (부분 일치)
      if card_type:
        query = query.filter(CardInfo.card_type.like(f"%{card_type}%"))
      
      # 카드사 ID로 필터링
      if card_company_id is not None:
        query = query.filter(CardInfo.card_company_id == card_company_id)
      
      # 사용여부로 필터링
      if is_active is not None:
        query = query.filter(CardInfo.is_active == is_active)
      
      results = query.all()
      return [card.to_dict() for card in results]
    except Exception as e:
      raise RuntimeError(f"카드 정보 검색 실패: {e}")

