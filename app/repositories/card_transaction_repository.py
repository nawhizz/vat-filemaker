"""
카드사용내역 Repository

card_transaction 테이블에 대한 CRUD 작업을 담당합니다.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
from app.repositories.schema import CardTransaction


class CardTransactionRepository:
    """
    카드사용내역 Repository 클래스
    
    카드사용내역을 관리합니다.
    """

    def __init__(self, session: Session):
        """Repository 초기화"""
        self.session = session

    def create(self, data: Dict[str, Any]) -> CardTransaction:
        """새로운 카드사용내역 생성"""
        try:
            entity = CardTransaction.from_dict(data)
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            # 제약조건 위반 시 더 명확한 에러 메시지 제공
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            raise ValueError(f"카드사용내역 저장 중 제약조건 위반이 발생했습니다: {error_msg}")
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"카드사용내역 저장 중 오류가 발생했습니다: {str(e)}")

    def get(self, entity_id: int) -> Optional[CardTransaction]:
        """ID로 단건 조회"""
        return self.session.query(CardTransaction).get(entity_id)

    def update(self, entity_id: int, update_data: Dict[str, Any]) -> Optional[CardTransaction]:
        """카드사용내역 수정"""
        try:
            entity = self.get(entity_id)
            if not entity:
                return None
            
            # transaction_date는 문자열에서 datetime으로 변환 필요
            if 'transaction_date' in update_data and isinstance(update_data['transaction_date'], str):
                from datetime import datetime
                try:
                    update_data['transaction_date'] = datetime.fromisoformat(
                        update_data['transaction_date'].replace('Z', '+00:00')
                    )
                except:
                    pass
            
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
        """카드사용내역 삭제"""
        entity = self.get(entity_id)
        if not entity:
            return False
        self.session.delete(entity)
        self.session.commit()
        return True

    def get_all(self) -> List[CardTransaction]:
        """전체 카드사용내역 조회"""
        return self.session.query(CardTransaction).all()

    def search(
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
    ) -> List[CardTransaction]:
        """
        카드사용내역 검색
        
        Args:
            card_company_id: 카드사 ID
            card_id: 카드 ID
            vendor_id: 거래처 ID
            transaction_date_from: 거래 일자 시작일
            transaction_date_to: 거래 일자 종료일
            is_cancel: 거래취소여부
            vendor_name: 거래처명 (부분 일치)
            business_number: 사업자등록번호
            approval_number: 승인번호
        """
        query = self.session.query(CardTransaction)
        
        # 필터 조건 추가
        conditions = []
        
        if card_company_id is not None:
            conditions.append(CardTransaction.card_company_id == card_company_id)
        
        if card_id is not None:
            conditions.append(CardTransaction.card_id == card_id)
        
        if vendor_id is not None:
            conditions.append(CardTransaction.vendor_id == vendor_id)
        
        if transaction_date_from:
            from datetime import datetime
            try:
                date_from = datetime.fromisoformat(transaction_date_from.replace('Z', '+00:00'))
                conditions.append(CardTransaction.transaction_date >= date_from)
            except:
                pass
        
        if transaction_date_to:
            from datetime import datetime
            try:
                date_to = datetime.fromisoformat(transaction_date_to.replace('Z', '+00:00'))
                conditions.append(CardTransaction.transaction_date <= date_to)
            except:
                pass
        
        if is_cancel is not None:
            conditions.append(CardTransaction.is_cancel == is_cancel)
        
        if vendor_name:
            conditions.append(CardTransaction.vendor_name.like(f'%{vendor_name}%'))
        
        if business_number:
            conditions.append(CardTransaction.business_number == business_number)
        
        if approval_number:
            conditions.append(CardTransaction.approval_number == approval_number)
        
        if conditions:
            query = query.filter(and_(*conditions))
        
        return query.order_by(CardTransaction.transaction_date.desc()).all()

