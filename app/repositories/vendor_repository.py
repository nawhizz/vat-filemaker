"""
거래처정보 Repository

vendor_info 테이블에 대한 CRUD 작업을 담당합니다.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.schema import VendorInfo


class VendorRepository:
    """
    거래처정보 Repository 클래스
    
    거래처 정보를 관리합니다.
    """

    def __init__(self, session: Session):
        """Repository 초기화"""
        self.session = session

    def create(self, data: Dict[str, Any]) -> VendorInfo:
        """새로운 거래처정보 생성"""
        try:
            entity = VendorInfo.from_dict(data)
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            # 제약조건 위반 시 더 명확한 에러 메시지 제공
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            raise ValueError(f"거래처 정보 저장 중 제약조건 위반이 발생했습니다: {error_msg}")
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"거래처 정보 저장 중 오류가 발생했습니다: {str(e)}")

    def get(self, entity_id: int) -> Optional[VendorInfo]:
        """ID로 단건 조회"""
        return self.session.query(VendorInfo).get(entity_id)

    def update(self, entity_id: int, update_data: Dict[str, Any]) -> Optional[VendorInfo]:
        """거래처정보 수정"""
        try:
            entity = self.get(entity_id)
            if not entity:
                return None
            
            from datetime import datetime
            
            for key, value in update_data.items():
                if hasattr(entity, key) and value is not None:
                    # DateTime 필드는 문자열인 경우 변환
                    if key == 'status_updated_at' and isinstance(value, str):
                        try:
                            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        except:
                            value = None
                    setattr(entity, key, value)
            
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            raise ValueError(f"거래처 정보 수정 중 제약조건 위반이 발생했습니다: {error_msg}")
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"거래처 정보 수정 중 오류가 발생했습니다: {str(e)}")

    def delete(self, entity_id: int) -> bool:
        """거래처정보 삭제"""
        entity = self.get(entity_id)
        if not entity:
            return False
        self.session.delete(entity)
        self.session.commit()
        return True

