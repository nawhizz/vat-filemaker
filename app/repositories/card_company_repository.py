"""
카드사정보 Repository

card_company_info 테이블에 대한 CRUD 작업을 담당합니다.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.schema import CardCompanyInfo


class CardCompanyRepository:
    """
    카드사정보 Repository 클래스
    
    카드사 메타 정보를 관리합니다.
    """

    def __init__(self, session: Session):
        """Repository 초기화"""
        self.session = session

    def create(self, data: Dict[str, Any]) -> CardCompanyInfo:
        """새로운 카드사정보 생성"""
        try:
            entity = CardCompanyInfo.from_dict(data)
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            # 제약조건 위반 시 더 명확한 에러 메시지 제공
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            raise ValueError(f"카드사 정보 저장 중 제약조건 위반이 발생했습니다: {error_msg}")
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"카드사 정보 저장 중 오류가 발생했습니다: {str(e)}")

    def get(self, entity_id: int) -> Optional[CardCompanyInfo]:
        """ID로 단건 조회"""
        return self.session.query(CardCompanyInfo).get(entity_id)


    def update(self, entity_id: int, update_data: Dict[str, Any]) -> Optional[CardCompanyInfo]:
        """카드사정보 수정"""
        try:
            entity = self.get(entity_id)
            if not entity:
                return None
            for key, value in update_data.items():
                if hasattr(entity, key) and value is not None:
                    setattr(entity, key, value)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            raise e

    def delete(self, entity_id: int) -> bool:
        """카드사정보 삭제"""
        entity = self.get(entity_id)
        if not entity:
            return False
        self.session.delete(entity)
        self.session.commit()
        return True

