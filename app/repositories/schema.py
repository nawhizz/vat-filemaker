"""
사업자정보 데이터 모델

SQLAlchemy ORM을 사용하여 사업자정보 테이블을 정의합니다.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class CommonCode(Base):
    """
    공통 코드 테이블 모델
    
    공통 코드(코드 그룹별 코드 값)를 저장합니다.
    """
    __tablename__ = 'common_code'
    
    # 복합 기본 키 (code_group, code)
    code_group = Column(String(100), primary_key=True, comment='코드 그룹명')
    code = Column(String(100), primary_key=True, comment='코드 값')
    
    # 코드명
    code_name = Column(String(255), nullable=False, comment='코드명')
    
    # 코드약어명
    code_abbr = Column(String(255), nullable=False, comment='코드약어명')
    
    # 정렬 순서
    sort_order = Column(Integer, default=0, comment='정렬 순서')
    
    # 사용여부 (Boolean: 0 = 비활성, 1 = 활성)
    is_active = Column(Boolean, default=True, nullable=False, comment='사용여부')
    
    # 비고
    description = Column(Text, comment='비고')
    
    # 생성/수정 시각
    created_at = Column(DateTime, default=func.current_timestamp(), comment='생성 시간')
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='최종 수정 시간'
    )
    
    def to_dict(self) -> dict:
        """객체를 딕셔너리로 변환합니다."""
        return {
            'code_group': self.code_group,
            'code': self.code,
            'code_name': self.code_name,
            'code_abbr': self.code_abbr,
            'sort_order': self.sort_order,
            'is_active': bool(self.is_active) if self.is_active is not None else True,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CommonCode':
        """딕셔너리로부터 객체를 생성합니다."""
        return cls(
            code_group=data.get('code_group'),
            code=data.get('code'),
            code_name=data.get('code_name'),
            code_abbr=data.get('code_abbr'),
            sort_order=data.get('sort_order', 0),
            is_active=data.get('is_active', True),
            description=data.get('description'),
        )


class BusinessInfo(Base):
    """
    사업자정보 테이블 모델
    
    개인 사업자의 기본 정보를 저장하는 테이블입니다.
    """
    
    __tablename__ = 'business_info'
    
    # 사업자등록번호 (Primary Key)
    business_number = Column(
        String(10), 
        primary_key=True, 
        comment='사업자등록번호'
    )
    
    # 사업자명
    business_name = Column(
        String(255), 
        nullable=False, 
        comment='사업자명'
    )
    
    # 대표자명
    owner_name = Column(
        String(100), 
        nullable=False, 
        comment='대표자명'
    )
    
    # 대표자주민등록번호 (Unique)
    owner_resident_number = Column(
        String(13), 
        unique=True, 
        comment='대표자주민등록번호'
    )
    
    # 업태
    business_type = Column(
        String(100), 
        comment='업태'
    )
    
    # 종목
    business_category = Column(
        String(100), 
        comment='종목'
    )
    
    # 주소
    address = Column(
        Text, 
        comment='주소'
    )
    
    # 전화번호
    phone_number = Column(
        String(20), 
        comment='전화번호'
    )
    
    # 이메일
    email = Column(
        String(255), 
        comment='이메일'
    )
    
    # 생성 시간
    created_at = Column(
        DateTime, 
        default=func.current_timestamp(), 
        comment='생성 시간'
    )
    
    # 최종 수정 시간
    updated_at = Column(
        DateTime, 
        default=func.current_timestamp(), 
        onupdate=func.current_timestamp(), 
        comment='최종 수정 시간'
    )

    
    def __repr__(self) -> str:
        """
        객체의 문자열 표현을 반환합니다.
        """
        return f"<BusinessInfo(business_number='{self.business_number}', business_name='{self.business_name}')>"
    
    def to_dict(self) -> dict:
        """
        객체를 딕셔너리로 변환합니다.
        """
        return {
            'business_number': self.business_number,
            'business_name': self.business_name,
            'owner_name': self.owner_name,
            'owner_resident_number': self.owner_resident_number,
            'business_type': self.business_type,
            'business_category': self.business_category,
            'address': self.address,
            'phone_number': self.phone_number,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BusinessInfo':
        """
        딕셔너리로부터 객체를 생성합니다.
        """
        return cls(
            business_number=data.get('business_number'),
            business_name=data.get('business_name'),
            owner_name=data.get('owner_name'),
            owner_resident_number=data.get('owner_resident_number'),
            business_type=data.get('business_type'),
            business_category=data.get('business_category'),
            address=data.get('address'),
            phone_number=data.get('phone_number'),
            email=data.get('email')
        )


class CardCompanyInfo(Base):
    """
    카드사 정보 테이블 모델
    
    카드사 메타 정보를 저장합니다.
    """
    __tablename__ = 'card_company_info'

    # 자동 생성 기본 키
    id = Column(Integer, primary_key=True, autoincrement=True, comment='기본 키')

    # 카드사 코드 및 명칭
    card_company_code = Column(String(3), nullable=False, comment='카드사 코드')
    card_company_name = Column(String(255), nullable=False, comment='카드사 한글명')
    card_company_name_en = Column(String(255), comment='카드사 영문명')

    # 생성/수정 시각
    created_at = Column(DateTime, default=func.current_timestamp(), comment='생성 시간')
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='최종 수정 시간'
    )

    def to_dict(self) -> dict:
        """객체를 딕셔너리로 변환합니다."""
        return {
            'id': self.id,
            'card_company_code': self.card_company_code,
            'card_company_name': self.card_company_name,
            'card_company_name_en': self.card_company_name_en,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CardCompanyInfo':
        """딕셔너리로부터 객체를 생성합니다."""
        return cls(
            card_company_code=data.get('card_company_code'),
            card_company_name=data.get('card_company_name'),
            card_company_name_en=data.get('card_company_name_en'),
        )


class CardInfo(Base):
    """
    카드 정보 테이블 모델
    
    카드 정보를 저장합니다.
    """
    __tablename__ = 'card_info'

    # 자동 생성 기본 키
    id = Column(Integer, primary_key=True, autoincrement=True, comment='기본 키')

    # 카드번호 (암호화된 값 저장)
    card_number = Column(String(255), nullable=False, comment='카드번호(암호화)')
    
    # 카드번호 (마스킹된 값 저장, 사용자 입력)
    masked_card_number = Column(String(50), nullable=True, comment='카드번호(마스킹)')

    # 카드명
    card_name = Column(String(255), nullable=False, comment='카드명')

    # 카드유형
    card_type = Column(String(50), comment='카드유형')

    # 참조: 카드사 ID (FK -> card_company_info.id)
    card_company_id = Column(Integer, ForeignKey('card_company_info.id'), nullable=False, comment='카드사 ID')

    # 사용여부 (Boolean: 0 = 비활성, 1 = 활성)
    is_active = Column(Boolean, default=True, nullable=False, comment='사용여부')

    # 생성/수정 시각
    created_at = Column(DateTime, default=func.current_timestamp(), comment='생성 시간')
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='최종 수정 시간'
    )

    # 관계 설정
    card_company = relationship("CardCompanyInfo", backref="cards")

    def to_dict(self) -> dict:
        """객체를 딕셔너리로 변환합니다."""
        return {
            'id': self.id,
            'card_number': self.card_number,
            'masked_card_number': self.masked_card_number,
            'card_name': self.card_name,
            'card_type': self.card_type,
            'card_company_id': self.card_company_id,
            'is_active': bool(self.is_active) if self.is_active is not None else True,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CardInfo':
        """딕셔너리로부터 객체를 생성합니다."""
        return cls(
            card_number=data.get('card_number'),
            masked_card_number=data.get('masked_card_number'),
            card_name=data.get('card_name'),
            card_type=data.get('card_type'),
            card_company_id=data.get('card_company_id'),
            is_active=data.get('is_active', True),
        )


class VendorInfo(Base):
    """
    거래처정보 테이블 모델
    
    거래처 정보를 저장합니다.
    """
    __tablename__ = 'vendor_info'
    
    # 자동 생성 기본 키
    id = Column(Integer, primary_key=True, autoincrement=True, comment='기본 키')
    
    # 거래처 사업자등록번호 (유니크)
    business_number = Column(String(10), unique=True, nullable=False, comment='거래처 사업자등록번호')
    
    # 거래처명
    vendor_name = Column(String(255), nullable=False, comment='거래처명')
    
    # 과세유형 (01:일반과세자, 02:간이과세자, 03:과세특례자, 04:면세사업자 등)
    tax_type = Column(String(10), comment='과세유형')
    
    # 사업자 상태 (01:계속사업자, 02:휴업, 03:폐업 등)
    business_status = Column(String(10), comment='사업자 상태')
    
    # 상태 업데이트 날짜
    status_updated_at = Column(DateTime, comment='상태 업데이트 날짜')
    
    # 생성/수정 시각
    created_at = Column(DateTime, default=func.current_timestamp(), comment='생성 시간')
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='최종 수정 시간'
    )
    
    def to_dict(self) -> dict:
        """객체를 딕셔너리로 변환합니다."""
        return {
            'id': self.id,
            'business_number': self.business_number,
            'vendor_name': self.vendor_name,
            'tax_type': self.tax_type,
            'business_status': self.business_status,
            'status_updated_at': self.status_updated_at.isoformat() if self.status_updated_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'VendorInfo':
        """딕셔너리로부터 객체를 생성합니다."""
        from datetime import datetime
        status_updated_at = data.get('status_updated_at')
        if isinstance(status_updated_at, str):
            try:
                status_updated_at = datetime.fromisoformat(status_updated_at.replace('Z', '+00:00'))
            except:
                status_updated_at = None
        
        return cls(
            business_number=data.get('business_number'),
            vendor_name=data.get('vendor_name'),
            tax_type=data.get('tax_type'),
            business_status=data.get('business_status'),
            status_updated_at=status_updated_at,
        )


class CardTransaction(Base):
    """
    카드사용내역 테이블 모델
    
    카드사용내역을 저장합니다.
    """
    __tablename__ = 'card_transaction'
    
    # 자동 생성 기본 키
    id = Column(Integer, primary_key=True, autoincrement=True, comment='기본 키')
    
    # 참조: 카드사 ID (FK -> card_company_info.id)
    card_company_id = Column(Integer, ForeignKey('card_company_info.id'), nullable=False, comment='카드사 ID')
    
    # 거래 일자
    transaction_date = Column(DateTime, nullable=False, comment='거래 일자')
    
    # 카드번호(마스킹)
    masked_card_number = Column(String(50), comment='카드번호(마스킹)')
    
    # 거래취소여부 (Boolean: FALSE/0 = 정상거래, TRUE/1 = 취소거래)
    is_cancel = Column(Boolean, default=False, nullable=False, comment='거래취소여부')
    
    # 거래 금액
    amount = Column(Numeric(15, 2), nullable=False, comment='거래 금액')
    
    # 거래처명
    vendor_name = Column(String(255), comment='거래처명')
    
    # 사업자등록번호
    business_number = Column(String(10), comment='사업자등록번호')
    
    # 승인번호
    approval_number = Column(String(20), comment='승인번호')
    
    # 참조: 카드 ID (FK -> card_info.id)
    card_id = Column(Integer, ForeignKey('card_info.id'), comment='카드 ID')
    
    # 참조: 거래처 ID (FK -> vendor_info.id)
    vendor_id = Column(Integer, ForeignKey('vendor_info.id'), comment='거래처 ID')
    
    # 생성/수정 시각
    created_at = Column(DateTime, default=func.current_timestamp(), comment='생성 시간')
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment='최종 수정 시간'
    )
    
    # 관계 설정
    card_company = relationship("CardCompanyInfo", backref="transactions")
    card = relationship("CardInfo", backref="transactions")
    vendor = relationship("VendorInfo", backref="transactions")
    
    def to_dict(self) -> dict:
        """객체를 딕셔너리로 변환합니다."""
        return {
            'id': self.id,
            'card_company_id': self.card_company_id,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'masked_card_number': self.masked_card_number,
            'is_cancel': bool(self.is_cancel) if self.is_cancel is not None else False,
            'amount': float(self.amount) if self.amount is not None else None,
            'vendor_name': self.vendor_name,
            'business_number': self.business_number,
            'approval_number': self.approval_number,
            'card_id': self.card_id,
            'vendor_id': self.vendor_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CardTransaction':
        """딕셔너리로부터 객체를 생성합니다."""
        from datetime import datetime
        transaction_date = data.get('transaction_date')
        if isinstance(transaction_date, str):
            try:
                transaction_date = datetime.fromisoformat(transaction_date.replace('Z', '+00:00'))
            except:
                transaction_date = None
        
        return cls(
            card_company_id=data.get('card_company_id'),
            transaction_date=transaction_date,
            masked_card_number=data.get('masked_card_number'),
            is_cancel=data.get('is_cancel', False),
            amount=data.get('amount'),
            vendor_name=data.get('vendor_name'),
            business_number=data.get('business_number'),
            approval_number=data.get('approval_number'),
            card_id=data.get('card_id'),
            vendor_id=data.get('vendor_id'),
        )
