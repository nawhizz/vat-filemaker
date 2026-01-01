"""
엑셀 파일 읽기 유틸리티

카드사용내역 엑셀 파일을 읽고 파싱하는 유틸리티 함수를 제공합니다.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import pandas as pd


def read_card_transaction_excel(
    file_path: str, 
    card_company_id: int,
    sheet_name: int = 0
) -> List[Dict[str, Any]]:
    """
    카드사용내역 엑셀 파일을 읽어서 딕셔너리 리스트로 변환
    
    엑셀 파일의 컬럼 매핑:
    - 거래일자 (또는 이용일) -> transaction_date
    - 카드번호 -> masked_card_number
    - 승인취소 (또는 구분) -> is_cancel
    - 이용금액 (또는 금액, 승인금액) -> amount
    - 가맹점명 (또는 거래처명) -> vendor_name
    - 사업자번호 (또는 사업자등록번호) -> business_number
    - 승인번호 -> approval_number
    
    Args:
        file_path: 엑셀 파일 경로
        card_company_id: 카드사 ID
        sheet_name: 시트 이름 또는 인덱스 (기본값: 0)
    
    Returns:
        카드사용내역 데이터 리스트
    
    Raises:
        FileNotFoundError: 파일이 존재하지 않는 경우
        ValueError: 파일 형식이 올바르지 않은 경우
    """
    # 파일 존재 여부 확인
    if not Path(file_path).exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # 컬럼명을 소문자로 변환하고 공백 제거
        df.columns = df.columns.str.strip().str.lower()
        
        # 컬럼 매핑 정의
        column_mapping = _get_column_mapping(df.columns.tolist())
        
        # 필수 컬럼 확인
        required_columns = ['transaction_date', 'amount']
        for col in required_columns:
            if col not in column_mapping:
                raise ValueError(f"필수 컬럼을 찾을 수 없습니다: {col}")
        
        # 데이터 변환
        transactions = []
        for _, row in df.iterrows():
            try:
                # 거래 일자 파싱
                transaction_date = _parse_transaction_date(
                    row.get(column_mapping.get('transaction_date'))
                )
                
                if not transaction_date:
                    continue  # 거래 일자가 없으면 스킵
                
                # 거래 금액 파싱
                amount = _parse_amount(
                    row.get(column_mapping.get('amount'))
                )
                
                if amount is None:
                    continue  # 금액이 없으면 스킵
                
                # 거래취소여부 파싱
                is_cancel = _parse_is_cancel(
                    row.get(column_mapping.get('is_cancel', ''))
                )
                
                # 사업자등록번호 정리
                business_number = _clean_business_number(
                    row.get(column_mapping.get('business_number', ''))
                )
                
                # 카드번호 마스킹 처리
                masked_card_number = str(row.get(column_mapping.get('masked_card_number', ''))).strip()
                
                # 거래처명
                vendor_name = str(row.get(column_mapping.get('vendor_name', ''))).strip()
                
                # 승인번호
                approval_number = str(row.get(column_mapping.get('approval_number', ''))).strip()
                
                # 딕셔너리 생성
                transaction = {
                    'card_company_id': card_company_id,
                    'transaction_date': transaction_date,
                    'masked_card_number': masked_card_number if masked_card_number else None,
                    'is_cancel': is_cancel,
                    'amount': amount,
                    'vendor_name': vendor_name if vendor_name else None,
                    'business_number': business_number,
                    'approval_number': approval_number if approval_number else None,
                    'card_id': None,  # 추후 매칭
                    'vendor_id': None,  # 추후 매칭
                }
                
                transactions.append(transaction)
                
            except Exception as e:
                # 특정 행 파싱 실패 시 스킵
                print(f"행 파싱 실패: {str(e)}")
                continue
        
        return transactions
        
    except Exception as e:
        raise ValueError(f"엑셀 파일 읽기 실패: {str(e)}")


def _get_column_mapping(columns: List[str]) -> Dict[str, str]:
    """
    엑셀 컬럼명을 내부 컬럼명으로 매핑
    
    Args:
        columns: 엑셀 파일의 컬럼명 리스트
    
    Returns:
        매핑 딕셔너리 {내부컬럼명: 엑셀컬럼명}
    """
    mapping = {}
    
    # 거래일자 매핑
    date_columns = ['거래일자', '이용일', '거래일', '승인일자', 'transaction_date', 'date']
    for col in columns:
        if any(dc in col for dc in date_columns):
            mapping['transaction_date'] = col
            break
    
    # 카드번호 매핑
    card_columns = ['카드번호', 'card_number', '카드']
    for col in columns:
        if any(cc in col for cc in card_columns):
            mapping['masked_card_number'] = col
            break
    
    # 거래취소여부 매핑
    cancel_columns = ['승인취소', '구분', '취소여부', 'status', '거래구분']
    for col in columns:
        if any(cc in col for cc in cancel_columns):
            mapping['is_cancel'] = col
            break
    
    # 거래금액 매핑
    amount_columns = ['이용금액', '금액', '승인금액', '거래금액', 'amount']
    for col in columns:
        if any(ac in col for ac in amount_columns):
            mapping['amount'] = col
            break
    
    # 거래처명 매핑
    vendor_columns = ['가맹점명', '거래처명', '상호', 'vendor', '가맹점']
    for col in columns:
        if any(vc in col for vc in vendor_columns):
            mapping['vendor_name'] = col
            break
    
    # 사업자등록번호 매핑
    business_columns = ['사업자번호', '사업자등록번호', 'business_number']
    for col in columns:
        if any(bc in col for bc in business_columns):
            mapping['business_number'] = col
            break
    
    # 승인번호 매핑
    approval_columns = ['승인번호', 'approval_number', '승인']
    for col in columns:
        if any(ac in col for ac in approval_columns):
            mapping['approval_number'] = col
            break
    
    return mapping


def _parse_transaction_date(value: Any) -> Optional[str]:
    """
    거래 일자를 ISO 형식 문자열로 변환
    
    Args:
        value: 거래 일자 값
    
    Returns:
        ISO 형식 문자열 (YYYY-MM-DDTHH:MM:SS) 또는 None
    """
    if pd.isna(value):
        return None
    
    try:
        # datetime 객체인 경우
        if isinstance(value, datetime):
            return value.isoformat()
        
        # 문자열인 경우 파싱 시도
        if isinstance(value, str):
            # 공백 제거
            value = value.strip()
            
            # 다양한 형식 시도
            formats = [
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%Y.%m.%d',
                '%Y%m%d',
                '%Y-%m-%d %H:%M:%S',
                '%Y/%m/%d %H:%M:%S',
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt.isoformat()
                except:
                    continue
        
        # pandas Timestamp로 변환 시도
        dt = pd.to_datetime(value)
        if not pd.isna(dt):
            return dt.isoformat()
        
    except:
        pass
    
    return None


def _parse_amount(value: Any) -> Optional[float]:
    """
    거래 금액을 float으로 변환
    
    Args:
        value: 거래 금액 값
    
    Returns:
        float 값 또는 None
    """
    if pd.isna(value):
        return None
    
    try:
        # 이미 숫자인 경우
        if isinstance(value, (int, float)):
            return float(value)
        
        # 문자열인 경우
        if isinstance(value, str):
            # 쉼표, 공백, 원화 기호 제거
            value = value.replace(',', '').replace(' ', '').replace('원', '').replace('₩', '')
            
            # 괄호로 감싸진 경우 음수로 처리
            if value.startswith('(') and value.endswith(')'):
                value = '-' + value[1:-1]
            
            return float(value)
        
    except:
        pass
    
    return None


def _parse_is_cancel(value: Any) -> bool:
    """
    거래취소여부를 boolean으로 변환
    
    Args:
        value: 거래취소여부 값
    
    Returns:
        True (취소) 또는 False (정상)
    """
    if pd.isna(value):
        return False
    
    # 문자열인 경우
    if isinstance(value, str):
        value = value.strip().lower()
        cancel_keywords = ['취소', 'cancel', '취', 'c']
        return any(keyword in value for keyword in cancel_keywords)
    
    return False


def _clean_business_number(value: Any) -> Optional[str]:
    """
    사업자등록번호를 정리 (하이픈 제거)
    
    Args:
        value: 사업자등록번호 값
    
    Returns:
        정리된 사업자등록번호 (10자리 숫자) 또는 None
    """
    if pd.isna(value):
        return None
    
    try:
        # 문자열로 변환
        value = str(value).strip()
        
        # 하이픈 및 공백 제거
        value = value.replace('-', '').replace(' ', '')
        
        # 10자리 숫자인지 확인
        if value.isdigit() and len(value) == 10:
            return value
        
    except:
        pass
    
    return None

