"""
부가세 도우미 메인 애플리케이션

PySide6-Fluent-Widgets를 사용한 부가세 신고 도우미 프로그램의 진입점입니다.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt
from app.views.main_window import MainWindow


def main() -> None:
    """
    메인 애플리케이션 진입점
    
    PySide6 애플리케이션을 초기화하고 메인 윈도우를 실행합니다.
    """
    # QApplication 인스턴스 생성
    app = QApplication(sys.argv)
    
    # 전체 애플리케이션 폰트 설정 (맑은 고딕)
    # 폰트 데이터베이스에서 사용 가능한 폰트 확인
    font_db = QFontDatabase()
    available_fonts = font_db.families()
    
    # 맑은 고딕 폰트 설정 (폰트 크기 명시)
    font_family = "맑은 고딕"
    if font_family not in available_fonts:
        # 맑은 고딕이 없으면 Malgun Gothic 시도 (영문명)
        font_family = "Malgun Gothic"
        if font_family not in available_fonts:
            # 둘 다 없으면 시스템 기본 폰트 사용
            system_font = QFont()
            font_family = system_font.family()
    
    font = QFont(font_family)
    font.setPointSize(9)  # 폰트 크기 명시
    app.setFont(font)
    
    # 스타일시트를 통한 전역 폰트 설정 (FluentWidgets 호환)
    app.setStyleSheet(f"""
        * {{
            font-family: "{font_family}", "Malgun Gothic", "맑은 고딕", sans-serif;
        }}
    """)
    
    # 애플리케이션 기본 설정
    app.setApplicationName("부가세 도우미")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("VAT FileMaker")
    
    # 고해상도 디스플레이 지원 (PySide6에서는 자동으로 처리됨)
    # app.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # deprecated
    # app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)     # deprecated
    
    # 메인 윈도우 생성 및 표시
    main_window = MainWindow()
    main_window.show()
    
    # 애플리케이션 실행
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
