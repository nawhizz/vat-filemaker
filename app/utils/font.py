"""
폰트 유틸리티 모듈

애플리케이션 전체에서 사용할 폰트 설정을 중앙 관리합니다.
"""

from PySide6.QtGui import QFont, QFontDatabase
from typing import Optional


# 폰트 설정 상수
DEFAULT_FONT_FAMILY = "맑은 고딕"
DEFAULT_FONT_FAMILY_EN = "Malgun Gothic"  # 영문명
DEFAULT_FONT_SIZE = 9  # 포인트


def get_available_font_family() -> str:
    """
    시스템에서 사용 가능한 폰트 패밀리 이름 반환
    
    기본 폰트(맑은 고딕)가 없으면 영문명(Malgun Gothic)을 시도하고,
    둘 다 없으면 시스템 기본 폰트를 반환합니다.
    
    Returns:
        사용 가능한 폰트 패밀리 이름
    """
    font_db = QFontDatabase()
    available_fonts = font_db.families()
    
    # 맑은 고딕 확인
    if DEFAULT_FONT_FAMILY in available_fonts:
        return DEFAULT_FONT_FAMILY
    
    # Malgun Gothic(영문명) 확인
    if DEFAULT_FONT_FAMILY_EN in available_fonts:
        return DEFAULT_FONT_FAMILY_EN
    
    # 둘 다 없으면 시스템 기본 폰트
    system_font = QFont()
    return system_font.family()


def get_app_font(size: Optional[int] = None) -> QFont:
    """
    애플리케이션 폰트 객체 생성
    
    Args:
        size: 폰트 크기 (포인트). None이면 기본 크기 사용
    
    Returns:
        QFont 객체
    """
    font_family = get_available_font_family()
    font = QFont(font_family)
    font.setPointSize(size if size is not None else DEFAULT_FONT_SIZE)
    return font


def get_font_stylesheet(size: Optional[int] = None) -> str:
    """
    폰트 스타일시트 문자열 생성
    
    FluentWidgets의 제목 위젯들(TitleLabel, SubtitleLabel 등)의 
    기본 폰트 크기는 유지하고, 폰트 패밀리만 적용합니다.
    
    Args:
        size: 폰트 크기 (포인트). None이면 폰트 크기는 각 위젯의 기본값 유지
    
    Returns:
        CSS 스타일시트 문자열
    """
    font_family = get_available_font_family()
    
    if size is not None:
        # 크기가 명시적으로 지정된 경우 폰트 크기도 적용
        return f"""
            * {{
                font-family: "{font_family}", "{DEFAULT_FONT_FAMILY_EN}", "{DEFAULT_FONT_FAMILY}", sans-serif;
                font-size: {size}pt;
            }}
        """
    else:
        # 크기가 지정되지 않은 경우 폰트 패밀리만 전역으로 설정
        # 각 위젯의 기본 폰트 크기는 유지됨 (TitleLabel=14pt, BodyLabel=9pt 등)
        return f"""
            * {{
                font-family: "{font_family}", "{DEFAULT_FONT_FAMILY_EN}", "{DEFAULT_FONT_FAMILY}", sans-serif;
            }}
        """


def get_table_font_stylesheet(size: Optional[int] = None) -> str:
    """
    TableView용 폰트 스타일시트 문자열 생성
    
    Args:
        size: 폰트 크기 (포인트). None이면 기본 크기 사용
    
    Returns:
        CSS 스타일시트 문자열
    """
    font_family = get_available_font_family()
    font_size = size if size is not None else DEFAULT_FONT_SIZE
    
    return f"""
        QTableView {{
            font-family: "{font_family}", "{DEFAULT_FONT_FAMILY_EN}", "{DEFAULT_FONT_FAMILY}", sans-serif;
            font-size: {font_size}pt;
        }}
        QHeaderView::section {{
            font-family: "{font_family}", "{DEFAULT_FONT_FAMILY_EN}", "{DEFAULT_FONT_FAMILY}", sans-serif;
            font-size: {font_size}pt;
        }}
    """

