"""
카드사용내역 서비스

카드사용내역 관련 비즈니스 로직을 처리합니다.
"""

from typing import Optional, Dict, Any, List
from app.repositories.database import DatabaseInitializer
from app.repositories.card_transaction_repository import CardTransactionRepository
from app.repositories.schema import CardTransaction
from app.config.settings import settings


class CardTransactionService:
  """
  카드사용내역 서비스 클래스
  
  카드사용내역 관련 비즈니스 로직을 담당합니다.
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
    self.repository: Optional[CardTransactionRepository] = None
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
      self.repository = CardTransactionRepository(session)
      
    except Exception as e:
      raise RuntimeError(f"데이터베이스 초기화 실패: {e}")
  
  def create_transaction(self, data: Dict[str, Any]) -> CardTransaction:
    """
    새로운 카드사용내역 생성
    
    Args:
      data: 카드사용내역 데이터
    
    Returns:
      생성된 CardTransaction 객체
    
    Raises:
      ValueError: 필수 필드가 누락된 경우
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    # 필수 필드 검사
    required_fields = ['card_company_id', 'transaction_date', 'amount']
    for field in required_fields:
      if not data.get(field):
        raise ValueError(f"{field}은(는) 필수 입력 항목입니다.")
    
    try:
      return self.repository.create(data)
    except ValueError as e:
      # 제약조건 위반 등의 ValueError는 그대로 전달
      raise e
    except Exception as e:
      raise RuntimeError(f"카드사용내역 생성 실패: {e}")
  
  def get_transaction(self, transaction_id: int) -> Optional[Dict[str, Any]]:
    """
    카드사용내역 조회
    
    Args:
      transaction_id: 카드사용내역 ID
    
    Returns:
      카드사용내역 딕셔너리 또는 None
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    transaction = self.repository.get(transaction_id)
    if not transaction:
      return None
    
    return transaction.to_dict()
  
  def update_transaction(self, transaction_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    카드사용내역 수정
    
    Args:
      transaction_id: 카드사용내역 ID
      update_data: 수정할 데이터
    
    Returns:
      수정된 카드사용내역 딕셔너리 또는 None
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      updated_transaction = self.repository.update(transaction_id, update_data)
      if not updated_transaction:
        return None
      
      return updated_transaction.to_dict()
    except Exception as e:
      raise RuntimeError(f"카드사용내역 수정 실패: {e}")
  
  def delete_transaction(self, transaction_id: int) -> bool:
    """
    카드사용내역 삭제
    
    Args:
      transaction_id: 카드사용내역 ID
    
    Returns:
      삭제 성공 여부
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      return self.repository.delete(transaction_id)
    except Exception as e:
      raise RuntimeError(f"카드사용내역 삭제 실패: {e}")
  
  def get_all_transactions(self) -> List[Dict[str, Any]]:
    """
    모든 카드사용내역 목록 조회
    
    Returns:
      카드사용내역 리스트
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      transactions = self.repository.get_all()
      return [transaction.to_dict() for transaction in transactions]
    except Exception as e:
      raise RuntimeError(f"카드사용내역 조회 실패: {e}")
  
  def search_transactions(
    self,
    card_company_id: Optional[int] = None,
    card_id: Optional[int] = None,
    vendor_id: Optional[int] = None,
    transaction_date_from: Optional[str] = None,
    transaction_date_to: Optional[str] = None,
    is_cancel: Optional[bool] = None,
    vendor_name: Optional[str] = None,
    business_number: Optional[str] = None,
    approval_number: Optional[str] = None
  ) -> List[Dict[str, Any]]:
    """
    카드사용내역 검색
    
    Args:
      card_company_id: 카드사 ID
      card_id: 카드 ID
      vendor_id: 거래처 ID
      transaction_date_from: 거래 일자 시작일 (YYYY-MM-DD 형식)
      transaction_date_to: 거래 일자 종료일 (YYYY-MM-DD 형식)
      is_cancel: 거래취소여부
      vendor_name: 거래처명 (부분 일치)
      business_number: 사업자등록번호
      approval_number: 승인번호
    
    Returns:
      검색된 카드사용내역 리스트
    """
    if not self.repository:
      raise RuntimeError("Repository가 초기화되지 않았습니다.")
    
    try:
      results = self.repository.search(
        card_company_id=card_company_id,
        card_id=card_id,
        vendor_id=vendor_id,
        transaction_date_from=transaction_date_from,
        transaction_date_to=transaction_date_to,
        is_cancel=is_cancel,
        vendor_name=vendor_name,
        business_number=business_number,
        approval_number=approval_number
      )
      return [transaction.to_dict() for transaction in results]
    except Exception as e:
      raise RuntimeError(f"카드사용내역 검색 실패: {e}")

