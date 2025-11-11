"""
암호화/복호화 유틸리티 모듈

카드번호 등 민감한 정보를 암호화/복호화하는 유틸리티 함수를 제공합니다.
Fernet 대칭 키 암호화를 사용합니다.
"""

import base64
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def generate_key_from_password(password: str, salt: bytes = b'vat_filemaker_salt') -> bytes:
    """
    비밀번호로부터 암호화 키 생성
    
    Args:
        password: 암호화 키 생성에 사용할 비밀번호
        salt: 솔트 (기본값 사용)
    
    Returns:
        Fernet 호환 키
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def get_fernet(key: Optional[str] = None) -> Fernet:
    """
    Fernet 암호화 객체 생성
    
    Args:
        key: 암호화 키 (None인 경우 설정에서 가져옴)
    
    Returns:
        Fernet 암호화 객체
    
    Raises:
        ValueError: 암호화 키가 없는 경우
    """
    from app.config.settings import settings
    
    if key is None:
        encryption_key = settings.ENCRYPTION_KEY
        if not encryption_key:
            raise ValueError("암호화 키가 설정되지 않았습니다. .env 파일에 ENCRYPTION_KEY를 설정하세요.")
    else:
        encryption_key = key
    
    # 키가 이미 Fernet 형식인지 확인 (44자 base64 문자열)
    if len(encryption_key) == 44:
        try:
            # Fernet 키 형식인 경우 직접 사용
            fernet_key = encryption_key.encode()
            # 키 유효성 검증
            Fernet(fernet_key)
            return Fernet(fernet_key)
        except Exception:
            # 유효하지 않은 키인 경우 비밀번호로부터 생성
            fernet_key = generate_key_from_password(encryption_key)
            return Fernet(fernet_key)
    else:
        # 비밀번호로부터 키 생성
        fernet_key = generate_key_from_password(encryption_key)
        return Fernet(fernet_key)


def encrypt_card_number(card_number: str, key: Optional[str] = None) -> str:
    """
    카드번호 암호화
    
    Args:
        card_number: 암호화할 카드번호 (평문)
        key: 암호화 키 (None인 경우 설정에서 가져옴)
    
    Returns:
        암호화된 카드번호 (base64 인코딩된 문자열)
    
    Raises:
        ValueError: 카드번호가 비어있거나 암호화 키가 없는 경우
    """
    if not card_number:
        raise ValueError("카드번호가 비어있습니다.")
    
    fernet = get_fernet(key)
    encrypted = fernet.encrypt(card_number.encode())
    return encrypted.decode('utf-8')


def decrypt_card_number(encrypted_card_number: str, key: Optional[str] = None) -> str:
    """
    카드번호 복호화
    
    Args:
        encrypted_card_number: 복호화할 카드번호 (암호화된 문자열)
        key: 암호화 키 (None인 경우 설정에서 가져옴)
    
    Returns:
        복호화된 카드번호 (평문)
    
    Raises:
        ValueError: 암호화된 카드번호가 비어있거나 암호화 키가 없는 경우
        Exception: 복호화 실패 시 (잘못된 키 등)
    """
    if not encrypted_card_number:
        raise ValueError("암호화된 카드번호가 비어있습니다.")
    
    fernet = get_fernet(key)
    try:
        decrypted = fernet.decrypt(encrypted_card_number.encode('utf-8'))
        return decrypted.decode('utf-8')
    except Exception as e:
        raise ValueError(f"카드번호 복호화 실패: {str(e)}")


def generate_fernet_key() -> str:
    """
    Fernet 호환 암호화 키 생성 (개발용)
    
    Returns:
        base64로 인코딩된 Fernet 키 (44자 문자열)
    """
    key = Fernet.generate_key()
    return key.decode('utf-8')


def format_card_number(card_number: str) -> str:
    """
    카드번호를 카드사별 형식에 맞게 포맷팅
    
    카드번호의 길이와 시작 번호(BIN)를 기준으로 자동으로 하이픈을 추가합니다.
    - 14자리 (다이너스클럽): xxxx-xxxxxx-xxxx
    - 15자리 (아멕스): xxxx-xxxxxx-xxxxx
    - 16자리 (일반카드): xxxx-xxxx-xxxx-xxxx
    
    Args:
        card_number: 포맷팅할 카드번호 (숫자만 또는 하이픈 포함)
    
    Returns:
        포맷팅된 카드번호
    """
    if not card_number:
        return ''
    
    # 하이픈 및 공백 제거
    clean_number = card_number.replace('-', '').replace(' ', '')
    
    # 숫자가 아닌 문자가 포함되어 있으면 원본 반환
    if not clean_number.isdigit():
        return card_number
    
    # 카드번호 길이에 따라 포맷팅
    length = len(clean_number)
    
    if length == 14:
        # 다이너스클럽: xxxx-xxxxxx-xxxx
        return f"{clean_number[:4]}-{clean_number[4:10]}-{clean_number[10:]}"
    elif length == 15:
        # 아멕스: xxxx-xxxxxx-xxxxx
        return f"{clean_number[:4]}-{clean_number[4:10]}-{clean_number[10:]}"
    elif length == 16:
        # 일반카드: xxxx-xxxx-xxxx-xxxx
        return f"{clean_number[:4]}-{clean_number[4:8]}-{clean_number[8:12]}-{clean_number[12:]}"
    else:
        # 기타 길이는 원본 반환 (아직 입력 중이거나 비표준 카드)
        return card_number


def clean_card_number(card_number: str) -> str:
    """
    카드번호에서 하이픈과 공백을 제거하여 숫자만 반환
    
    Args:
        card_number: 정리할 카드번호
    
    Returns:
        숫자만 포함된 카드번호
    """
    if not card_number:
        return ''
    
    return card_number.replace('-', '').replace(' ', '')


def get_card_type_and_max_length(card_number: str) -> tuple[str, int]:
    """
    카드번호의 시작 번호(BIN)를 기반으로 카드 유형과 최대 자리수를 반환
    
    Args:
        card_number: 카드번호 (숫자만 또는 하이픈 포함)
    
    Returns:
        (카드 유형, 최대 자리수) 튜플
        - 아멕스: ('AMEX', 15)
        - 다이너스클럽: ('DINERS', 14)
        - 일반카드: ('STANDARD', 16)
    """
    if not card_number:
        return ('STANDARD', 16)
    
    # 숫자만 추출
    clean_number = clean_card_number(card_number)
    
    if not clean_number.isdigit():
        return ('STANDARD', 16)
    
    # 시작 번호(BIN) 확인
    if len(clean_number) >= 2:
        bin_2 = clean_number[:2]
        
        # 아멕스: 34, 37로 시작
        if bin_2 in ['34', '37']:
            return ('AMEX', 15)
        
        # 다이너스클럽: 36으로 시작
        if bin_2 == '36':
            return ('DINERS', 14)
        
        # 다이너스클럽: 3616 등으로 시작 (4자리 확인)
        if len(clean_number) >= 4:
            bin_4 = clean_number[:4]
            if bin_4.startswith('36'):
                return ('DINERS', 14)
    
    # 기본값: 일반카드 (비자, 마스터 등)
    return ('STANDARD', 16)

