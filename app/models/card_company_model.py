"""
카드사 정보 테이블 모델

QAbstractTableModel을 상속받아 카드사 정보를 테이블에 표시하기 위한 모델입니다.
"""

from typing import List, Dict, Any, Optional
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex


class CardCompanyModel(QAbstractTableModel):
  """
  카드사 정보 테이블 모델 클래스
  
  QAbstractTableModel을 상속받아 카드사 정보를 테이블 뷰에 표시합니다.
  """
  
  # 컬럼 헤더 정의
  COLUMN_HEADERS = [
    "ID",
    "카드사 코드",
    "카드사 한글명",
    "카드사 영문명",
    "생성일시",
    "수정일시"
  ]
  
  # 컬럼 인덱스 상수
  COL_ID = 0
  COL_CARD_COMPANY_CODE = 1
  COL_CARD_COMPANY_NAME = 2
  COL_CARD_COMPANY_NAME_EN = 3
  COL_CREATED_AT = 4
  COL_UPDATED_AT = 5
  
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
    
    card_company = self._data[row]
    
    if role == Qt.ItemDataRole.DisplayRole:
      if col == self.COL_ID:
        return card_company.get('id', '')
      elif col == self.COL_CARD_COMPANY_CODE:
        return card_company.get('card_company_code', '')
      elif col == self.COL_CARD_COMPANY_NAME:
        return card_company.get('card_company_name', '')
      elif col == self.COL_CARD_COMPANY_NAME_EN:
        return card_company.get('card_company_name_en', '')
      elif col == self.COL_CREATED_AT:
        created_at = card_company.get('created_at', '')
        if created_at:
          # ISO 형식 문자열을 간단한 형식으로 변환
          if isinstance(created_at, str):
            return created_at[:19] if len(created_at) >= 19 else created_at
        return created_at
      elif col == self.COL_UPDATED_AT:
        updated_at = card_company.get('updated_at', '')
        if updated_at:
          # ISO 형식 문자열을 간단한 형식으로 변환
          if isinstance(updated_at, str):
            return updated_at[:19] if len(updated_at) >= 19 else updated_at
        return updated_at
    
    elif role == Qt.ItemDataRole.TextAlignmentRole:
      # 숫자 컬럼은 우측 정렬, 나머지는 좌측 정렬
      if col == self.COL_ID:
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
      data: 카드사 정보 리스트
    """
    self.beginResetModel()
    self._data = data.copy() if data else []
    self.endResetModel()
  
  def get_data(self) -> List[Dict[str, Any]]:
    """
    현재 모델 데이터 반환
    
    Returns:
      카드사 정보 리스트
    """
    return self._data.copy()
  
  def get_row_data(self, row: int) -> Optional[Dict[str, Any]]:
    """
    특정 행의 데이터 반환
    
    Args:
      row: 행 인덱스
    
    Returns:
      해당 행의 카드사 정보 또는 None
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

