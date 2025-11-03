"""
공통코드 Repository

common_code 테이블에 대한 CRUD 작업을 담당합니다.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.schema import CommonCode


class CommonCodeRepository:
    """
    공통코드 Repository 클래스
    
    공통 코드를 관리합니다.
    """

    def __init__(self, session: Session):
        """Repository 초기화"""
        self.session = session

    def create(self, data: Dict[str, Any]) -> CommonCode:
        """새로운 공통코드 생성"""
        try:
            entity = CommonCode.from_dict(data)
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            # 제약조건 위반 시 더 명확한 에러 메시지 제공
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            raise ValueError(f"공통 코드 저장 중 제약조건 위반이 발생했습니다: {error_msg}")
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"공통 코드 저장 중 오류가 발생했습니다: {str(e)}")

    def get(self, code_group: str, code: str) -> Optional[CommonCode]:
        """복합 키(code_group, code)로 단건 조회"""
        return self.session.query(CommonCode).filter(
            CommonCode.code_group == code_group,
            CommonCode.code == code
        ).first()

    def update(self, code_group: str, code: str, update_data: Dict[str, Any]) -> Optional[CommonCode]:
        """공통코드 수정"""
        try:
            entity = self.get(code_group, code)
            if not entity:
                return None
            
            # 복합 키는 수정할 수 없으므로 제외
            for key, value in update_data.items():
                if key not in ['code_group', 'code'] and hasattr(entity, key) and value is not None:
                    setattr(entity, key, value)
            
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            raise ValueError(f"공통 코드 수정 중 제약조건 위반이 발생했습니다: {error_msg}")
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"공통 코드 수정 중 오류가 발생했습니다: {str(e)}")

    def delete(self, code_group: str, code: str) -> bool:
        """공통코드 삭제"""
        entity = self.get(code_group, code)
        if not entity:
            return False
        self.session.delete(entity)
        self.session.commit()
        return True

    def get_by_group(self, code_group: str) -> List[CommonCode]:
        """코드 그룹으로 조회"""
        return self.session.query(CommonCode).filter(
            CommonCode.code_group == code_group
        ).order_by(CommonCode.sort_order).all()

    def get_all(self) -> List[CommonCode]:
        """전체 조회"""
        return self.session.query(CommonCode).order_by(
            CommonCode.code_group, CommonCode.sort_order
        ).all()

