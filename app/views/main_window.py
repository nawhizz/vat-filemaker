"""
부가세 도우미 메인 윈도우

PySide6-Fluent-Widgets를 사용하여 Fluent Design 스타일의 메인 윈도우를 구현합니다.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import (
    FluentWindow, 
    NavigationItemPosition,
    FluentIcon,
    PrimaryPushButton,
    PushButton,
    InfoBar,
    InfoBarPosition
)
from app.views.business_registration_view import BusinessRegistrationInterface
from app.views.card_company_view import CardCompanyInterface
from app.views.card_view import CardInterface
from app.views.common_code_view import CommonCodeInterface
from app.views.vendor_view import VendorInterface


class MainWindow(FluentWindow):
    """
    부가세 도우미 메인 윈도우 클래스
    
    FluentWindow를 상속받아 Fluent Design 스타일의 윈도우를 구현합니다.
    """
    
    def __init__(self):
        super().__init__()
        
        # 윈도우 기본 설정
        self.setWindowTitle("부가세 도우미")
        self.setMinimumSize(1024, 768)
        self.resize(1280, 800)  # 최초 실행시 윈도우 크기 설정
        
        # 네비게이션 아이템 추가
        self._init_navigation()
        
        # 메인 콘텐츠 설정
        self._init_main_content()
        
        # 윈도우 중앙에 배치
        self.center_window()
    
    def _init_navigation(self) -> None:
        """
        네비게이션 메뉴 초기화
        
        FluentWindow의 네비게이션 인터페이스를 설정합니다.
        """
        # 홈 페이지 추가
        self.home_interface = HomeInterface()
        self.home_interface.setObjectName("home_interface")
        self.addSubInterface(
            self.home_interface,
            FluentIcon.HOME,
            "홈",
            NavigationItemPosition.TOP
        )
        
        # 사업장 정보 등록 페이지 추가
        self.business_registration_interface = BusinessRegistrationInterface()
        self.business_registration_interface.setObjectName("business_registration_interface")
        self.addSubInterface(
            self.business_registration_interface,
            FluentIcon.PEOPLE,
            "사업자자 정보 관리",
            NavigationItemPosition.TOP
        )
        
        # 카드사 정보 관리 페이지 추가
        self.card_company_interface = CardCompanyInterface()
        self.card_company_interface.setObjectName("card_company_interface")
        self.addSubInterface(
            self.card_company_interface,
            FluentIcon.CAFE,
            "카드사 정보 관리",
            NavigationItemPosition.TOP
        )
        
        # 카드 정보 등록 페이지 추가
        self.card_interface = CardInterface()
        self.card_interface.setObjectName("card_interface")
        self.addSubInterface(
            self.card_interface,
            FluentIcon.CHAT,
            "카드 정보 관리",
            NavigationItemPosition.TOP
        )
        
        # 공통코드 관리 페이지 추가
        self.common_code_interface = CommonCodeInterface()
        self.common_code_interface.setObjectName("common_code_interface")
        self.addSubInterface(
            self.common_code_interface,
            FluentIcon.DEVELOPER_TOOLS,
            "공통코드 관리",
            NavigationItemPosition.TOP
        )
        
        # 거래처정보 관리 페이지 추가
        self.vendor_interface = VendorInterface()
        self.vendor_interface.setObjectName("vendor_interface")
        self.addSubInterface(
            self.vendor_interface,
            FluentIcon.SHOPPING_CART,
            "거래처정보 관리",
            NavigationItemPosition.TOP
        )
        
        # 설정 페이지 추가
        self.settings_interface = SettingsInterface()
        self.settings_interface.setObjectName("settings_interface")
        self.addSubInterface(
            self.settings_interface,
            FluentIcon.SETTING,
            "설정",
            NavigationItemPosition.BOTTOM
        )
    
    def _init_main_content(self) -> None:
        """
        메인 콘텐츠 초기화
        
        홈 인터페이스를 기본으로 설정합니다.
        """
        self.stackedWidget.setCurrentWidget(self.home_interface)
    
    def center_window(self) -> None:
        """
        윈도우를 화면 중앙에 배치
        
        화면 크기를 기준으로 윈도우를 중앙에 위치시킵니다.
        """
        from PySide6.QtGui import QGuiApplication
        
        screen = QGuiApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )


class HomeInterface(QWidget):
    """
    홈 인터페이스
    
    메인 화면의 홈 페이지를 구현합니다.
    """
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self) -> None:
        """
        홈 인터페이스 UI 초기화
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 환영 메시지
        welcome_label = QLabel("부가세 도우미에 오신 것을 환영합니다!")
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(welcome_label)
        
        # 설명 텍스트
        description_label = QLabel("""
        이 프로그램을 통해 다음과 같은 작업을 수행할 수 있습니다:
        
        • 카드 사용 내역 엑셀 파일 업로드 및 관리
        • 사업자 상태 조회 및 관리
        • 부가세 제외 대상 거래 관리
        • 부가세 신고용 전자 매체 파일 생성
        """)
        description_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666666;
                line-height: 1.6;
            }
        """)
        layout.addWidget(description_label)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # 사업장 정보 등록 버튼
        business_registration_button = PrimaryPushButton("사업장 정보 등록")
        business_registration_button.clicked.connect(self._on_business_registration_button_clicked)
        button_layout.addWidget(business_registration_button)
        
        # 엑셀 파일 업로드 버튼
        upload_button = PushButton("엑셀 파일 업로드")
        upload_button.clicked.connect(self._on_upload_button_clicked)
        button_layout.addWidget(upload_button)
        
        # 사업자 조회 버튼
        taxpayer_button = PushButton("사업자 상태 조회")
        taxpayer_button.clicked.connect(self._on_taxpayer_button_clicked)
        button_layout.addWidget(taxpayer_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def _on_business_registration_button_clicked(self) -> None:
        """
        사업장 정보 등록 버튼 클릭 이벤트 처리
        """
        # 메인 윈도우의 네비게이션을 사업장 정보 등록 페이지로 변경
        main_window = self.parent()
        while main_window and not isinstance(main_window, FluentWindow):
            main_window = main_window.parent()
        
        if main_window:
            main_window.stackedWidget.setCurrentWidget(main_window.business_registration_interface)
    
    def _on_upload_button_clicked(self) -> None:
        """
        엑셀 파일 업로드 버튼 클릭 이벤트 처리
        """
        InfoBar.success(
            title="알림",
            content="엑셀 파일 업로드 기능이 곧 구현될 예정입니다.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )
    
    def _on_taxpayer_button_clicked(self) -> None:
        """
        사업자 상태 조회 버튼 클릭 이벤트 처리
        """
        InfoBar.info(
            title="알림",
            content="사업자 상태 조회 기능이 곧 구현될 예정입니다.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )


class SettingsInterface(QWidget):
    """
    설정 인터페이스
    
    애플리케이션 설정을 관리하는 페이지입니다.
    """
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self) -> None:
        """
        설정 인터페이스 UI 초기화
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title_label = QLabel("설정")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title_label)
        
        placeholder_label = QLabel("설정 기능이 곧 구현될 예정입니다.")
        placeholder_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666666;
            }
        """)
        layout.addWidget(placeholder_label)
        layout.addStretch()
