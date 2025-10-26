"""
사업장정보 데이터 모델

SQLAlchemy ORM을 사용하여 사업장정보 테이블을 정의합니다.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BusinessInfo(Base):
    """
    사업장정보 테이블 모델
    
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
