"""
카드사용내역 테이블 모델

QAbstractTableModel을 상속받아 카드사용내역을 테이블에 표시하기 위한 모델입니다.
"""

from typing import List, Dict, Any, Optional
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from datetime import datetime


class CardTransactionModel(QAbstractTableModel):
  """
  카드사용내역 테이블 모델 클래스
  
  QAbstractTableModel을 상속받아 카드사용내역을 테이블 뷰에 표시합니다.
  """
  
  # 컬럼 헤더 정의
  COLUMN_HEADERS = [
    "ID",
    "카드사 ID",
    "거래 일자",
    "마스킹 카드번호",
    "거래취소여부",
    "거래 금액",
    "거래처명",
    "사업자등록번호",
    "승인번호",
    "카드 ID",
    "거래처 ID",
    "생성일시",
    "수정일시"
  ]
  
  # 컬럼 인덱스 상수
  COL_ID = 0
  COL_CARD_COMPANY_ID = 1
  COL_TRANSACTION_DATE = 2
  COL_MASKED_CARD_NUMBER = 3
  COL_IS_CANCEL = 4
  COL_AMOUNT = 5
  COL_VENDOR_NAME = 6
  COL_BUSINESS_NUMBER = 7
  COL_APPROVAL_NUMBER = 8
  COL_CARD_ID = 9
  COL_VENDOR_ID = 10
  COL_CREATED_AT = 11
  COL_UPDATED_AT = 12
  
  def __init__(self, parent=None):
    """
    모델 초기화
    
    Args:
      parent: 부모 객체
    """
    super().__init__(parent)
    self._data: List[Dict[str, Any]] = []
  
  def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
    """
    행 개수 반환
    
    Args:
      parent: 부모 인덱스
    
    Returns:
      행 개수
    """
    return len(self._data)
  
  def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
    """
    열 개수 반환
    
    Args:
      parent: 부모 인덱스
    
    Returns:
      열 개수
    """
    return len(self.COLUMN_HEADERS)
  
  def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
    """
    인덱스 위치의 데이터 반환
    
    Args:
      index: 데이터 인덱스
      role: 데이터 역할
    
    Returns:
      인덱스 위치의 데이터
    """
    if not index.isValid():
      return None
    
    row = index.row()
    col = index.column()
    
    if row >= len(self._data):
      return None
    
    transaction = self._data[row]
    
    if role == Qt.ItemDataRole.DisplayRole:
      if col == self.COL_ID:
        return transaction.get('id', '')
      elif col == self.COL_CARD_COMPANY_ID:
        return transaction.get('card_company_id', '')
      elif col == self.COL_TRANSACTION_DATE:
        transaction_date = transaction.get('transaction_date', '')
        if transaction_date:
          # ISO 형식 문자열을 간단한 형식으로 변환
          if isinstance(transaction_date, str):
            try:
              dt = datetime.fromisoformat(transaction_date.replace('Z', '+00:00'))
              return dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
              return transaction_date[:19] if len(transaction_date) >= 19 else transaction_date
        return transaction_date
      elif col == self.COL_MASKED_CARD_NUMBER:
        return transaction.get('masked_card_number', '')
      elif col == self.COL_IS_CANCEL:
        is_cancel = transaction.get('is_cancel', False)
        return "취소" if is_cancel else "정상"
      elif col == self.COL_AMOUNT:
        amount = transaction.get('amount')
        if amount is not None:
          # 금액을 천단위 구분자와 함께 표시
          return f"{float(amount):,.0f}"
        return ''
      elif col == self.COL_VENDOR_NAME:
        return transaction.get('vendor_name', '')
      elif col == self.COL_BUSINESS_NUMBER:
        business_number = transaction.get('business_number', '')
        # 사업자등록번호 포맷팅 (xxx-xx-xxxxx)
        if business_number and len(business_number) == 10:
          return f"{business_number[:3]}-{business_number[3:5]}-{business_number[5:]}"
        return business_number
      elif col == self.COL_APPROVAL_NUMBER:
        return transaction.get('approval_number', '')
      elif col == self.COL_CARD_ID:
        return transaction.get('card_id', '')
      elif col == self.COL_VENDOR_ID:
        return transaction.get('vendor_id', '')
      elif col == self.COL_CREATED_AT:
        created_at = transaction.get('created_at', '')
        if created_at:
          # ISO 형식 문자열을 간단한 형식으로 변환
          if isinstance(created_at, str):
            return created_at[:19] if len(created_at) >= 19 else created_at
        return created_at
      elif col == self.COL_UPDATED_AT:
        updated_at = transaction.get('updated_at', '')
        if updated_at:
          # ISO 형식 문자열을 간단한 형식으로 변환
          if isinstance(updated_at, str):
            return updated_at[:19] if len(updated_at) >= 19 else updated_at
        return updated_at
    
    elif role == Qt.ItemDataRole.TextAlignmentRole:
      # 숫자 컬럼은 우측 정렬, 나머지는 좌측 정렬
      if col in [self.COL_ID, self.COL_CARD_COMPANY_ID, self.COL_CARD_ID, self.COL_VENDOR_ID, self.COL_AMOUNT]:
        return int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
      else:
        return int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    
    return None
  
  def headerData(
    self, 
    section: int, 
    orientation: Qt.Orientation, 
    role: int = Qt.ItemDataRole.DisplayRole
  ) -> Any:
    """
    헤더 데이터 반환
    
    Args:
      section: 섹션 인덱스
      orientation: 방향 (가로/세로)
      role: 데이터 역할
    
    Returns:
      헤더 데이터
    """
    if role == Qt.ItemDataRole.DisplayRole:
      if orientation == Qt.Orientation.Horizontal:
        if 0 <= section < len(self.COLUMN_HEADERS):
          return self.COLUMN_HEADERS[section]
    
    return None
  
  def set_data(self, data: List[Dict[str, Any]]) -> None:
    """
    모델 데이터 설정
    
    Args:
      data: 카드사용내역 리스트
    """
    self.beginResetModel()
    self._data = data.copy() if data else []
    self.endResetModel()
  
  def get_data(self) -> List[Dict[str, Any]]:
    """
    현재 모델 데이터 반환
    
    Returns:
      카드사용내역 리스트
    """
    return self._data.copy()
  
  def get_row_data(self, row: int) -> Optional[Dict[str, Any]]:
    """
    특정 행의 데이터 반환
    
    Args:
      row: 행 인덱스
    
    Returns:
      해당 행의 카드사용내역 또는 None
    """
    if 0 <= row < len(self._data):
      return self._data[row].copy()
    return None
  
  def clear(self) -> None:
    """
    모델 데이터 초기화
    """
    self.beginResetModel()
    self._data = []
    self.endResetModel()

