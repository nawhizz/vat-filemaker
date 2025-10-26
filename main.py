"""
부가세 도우미 메인 애플리케이션

PySide6-Fluent-Widgets를 사용한 부가세 신고 도우미 프로그램의 진입점입니다.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from app.views.main_window import MainWindow


def main() -> None:
    """
    메인 애플리케이션 진입점
    
    PySide6 애플리케이션을 초기화하고 메인 윈도우를 실행합니다.
    """
    # QApplication 인스턴스 생성
    app = QApplication(sys.argv)
    
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
