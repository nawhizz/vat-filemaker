"""
거래처정보 테이블 모델

QAbstractTableModel을 상속받아 거래처정보를 테이블에 표시하기 위한 모델입니다.
"""

from typing import List, Dict, Any, Optional
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex


class VendorModel(QAbstractTableModel):
    """
    거래처정보 테이블 모델 클래스
    
    QAbstractTableModel을 상속받아 거래처정보를 테이블 뷰에 표시합니다.
    """
    
    # 컬럼 헤더 정의
    COLUMN_HEADERS = [
        "ID",
        "사업자등록번호",
        "거래처명",
        "과세유형",
        "사업자 상태",
        "상태 업데이트일",
        "생성일시",
        "수정일시"
    ]
    
    # 컬럼 인덱스 상수
    COL_ID = 0
    COL_BUSINESS_NUMBER = 1
    COL_VENDOR_NAME = 2
    COL_TAX_TYPE = 3
    COL_BUSINESS_STATUS = 4
    COL_STATUS_UPDATED_AT = 5
    COL_CREATED_AT = 6
    COL_UPDATED_AT = 7
    
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
        
        vendor = self._data[row]
        
        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.COL_ID:
                return vendor.get('id', '')
            elif col == self.COL_BUSINESS_NUMBER:
                # 사업자등록번호를 xxx-xx-xxxxx 형식으로 포맷팅
                business_number = vendor.get('business_number', '')
                if business_number:
                    # 하이픈 제거한 순수 숫자
                    clean_number = business_number.replace('-', '')
                    if len(clean_number) == 10 and clean_number.isdigit():
                        return f"{clean_number[:3]}-{clean_number[3:5]}-{clean_number[5:]}"
                return business_number
            elif col == self.COL_VENDOR_NAME:
                return vendor.get('vendor_name', '')
            elif col == self.COL_TAX_TYPE:
                # 코드명이 있으면 코드명 표시, 없으면 코드 표시
                tax_type_name = vendor.get('tax_type_name')
                return tax_type_name if tax_type_name else vendor.get('tax_type', '')
            elif col == self.COL_BUSINESS_STATUS:
                # 코드명이 있으면 코드명 표시, 없으면 코드 표시
                business_status_name = vendor.get('business_status_name')
                return business_status_name if business_status_name else vendor.get('business_status', '')
            elif col == self.COL_STATUS_UPDATED_AT:
                status_updated_at = vendor.get('status_updated_at', '')
                if status_updated_at:
                    # ISO 형식 문자열을 간단한 형식으로 변환
                    if isinstance(status_updated_at, str):
                        return status_updated_at[:19] if len(status_updated_at) >= 19 else status_updated_at
                return status_updated_at
            elif col == self.COL_CREATED_AT:
                created_at = vendor.get('created_at', '')
                if created_at:
                    # ISO 형식 문자열을 간단한 형식으로 변환
                    if isinstance(created_at, str):
                        return created_at[:19] if len(created_at) >= 19 else created_at
                return created_at
            elif col == self.COL_UPDATED_AT:
                updated_at = vendor.get('updated_at', '')
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
            data: 거래처정보 리스트
        """
        self.beginResetModel()
        self._data = data.copy() if data else []
        self.endResetModel()
    
    def get_data(self) -> List[Dict[str, Any]]:
        """
        현재 모델 데이터 반환
        
        Returns:
            거래처정보 리스트
        """
        return self._data.copy()
    
    def get_row_data(self, row: int) -> Optional[Dict[str, Any]]:
        """
        특정 행의 데이터 반환
        
        Args:
            row: 행 인덱스
        
        Returns:
            해당 행의 거래처정보 또는 None
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

