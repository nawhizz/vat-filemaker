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

