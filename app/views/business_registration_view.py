"""
사업장 정보 등록 인터페이스

사업장 정보를 등록하고 수정하는 페이지를 구현합니다.
"""

from typing import Optional, Dict, Any
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QTextEdit
from qfluentwidgets import (
    PrimaryPushButton, 
    PushButton, 
    LineEdit, 
    TextEdit, 
    InfoBar, 
    InfoBarPosition,
    CardWidget,
    TitleLabel,
    BodyLabel
)
from app.services.business_service import BusinessService


class BusinessRegistrationInterface(QWidget):
    """
    사업장 정보 등록 인터페이스
    
    사업장 정보를 등록하고 관리하는 페이지입니다.
    """
    
    # 데이터 변경 시그널
    data_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.business_service = BusinessService()
        self.current_business_number: Optional[str] = None
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self) -> None:
        """
        사업장 정보 등록 인터페이스 UI 초기화
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 제목
        title_label = TitleLabel("사업장 정보 등록")
        layout.addWidget(title_label)
        
        # 설명
        description_label = BodyLabel("사업장의 기본 정보를 입력하여 등록하세요.")
        layout.addWidget(description_label)
        
        # 입력 폼 카드
        form_card = CardWidget()
        form_card.setFixedHeight(500)
        form_layout = QFormLayout(form_card)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # 사업자등록번호
        self.business_number_input = LineEdit()
        self.business_number_input.setPlaceholderText("예: 123-45-67890")
        self.business_number_input.setMaxLength(12)  # 하이픈 포함 최대 길이
        # 숫자와 하이픈만 입력 가능하도록 설정
        self.business_number_input.setValidator(None)  # 기본 검증기 제거
        form_layout.addRow("사업자등록번호 *", self.business_number_input)
        
        # 사업자명
        self.business_name_input = LineEdit()
        self.business_name_input.setPlaceholderText("사업자명을 입력하세요")
        self.business_name_input.setMaxLength(255)
        form_layout.addRow("사업자명 *", self.business_name_input)
        
        # 대표자명
        self.owner_name_input = LineEdit()
        self.owner_name_input.setPlaceholderText("대표자명을 입력하세요")
        self.owner_name_input.setMaxLength(100)
        form_layout.addRow("대표자명 *", self.owner_name_input)
        
        # 대표자주민등록번호
        self.owner_resident_number_input = LineEdit()
        self.owner_resident_number_input.setPlaceholderText("예: 123456-1234567")
        self.owner_resident_number_input.setMaxLength(14)  # 하이픈 포함
        form_layout.addRow("대표자주민등록번호", self.owner_resident_number_input)
        
        # 업태
        self.business_type_input = LineEdit()
        self.business_type_input.setPlaceholderText("업태를 입력하세요")
        self.business_type_input.setMaxLength(100)
        form_layout.addRow("업태", self.business_type_input)
        
        # 종목
        self.business_category_input = LineEdit()
        self.business_category_input.setPlaceholderText("종목을 입력하세요")
        self.business_category_input.setMaxLength(100)
        form_layout.addRow("종목", self.business_category_input)
        
        # 주소
        self.address_input = TextEdit()
        self.address_input.setPlaceholderText("주소를 입력하세요")
        self.address_input.setMaximumHeight(80)
        form_layout.addRow("주소", self.address_input)
        
        # 전화번호
        self.phone_number_input = LineEdit()
        self.phone_number_input.setPlaceholderText("예: 02-1234-5678")
        self.phone_number_input.setMaxLength(20)
        form_layout.addRow("전화번호", self.phone_number_input)
        
        # 이메일
        self.email_input = LineEdit()
        self.email_input.setPlaceholderText("예: example@email.com")
        self.email_input.setMaxLength(255)
        form_layout.addRow("이메일", self.email_input)
        
        layout.addWidget(form_card)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # 등록 버튼
        self.register_button = PrimaryPushButton("등록")
        self.register_button.clicked.connect(self._on_register_button_clicked)
        button_layout.addWidget(self.register_button)
        
        # 수정 버튼
        self.update_button = PushButton("수정")
        self.update_button.clicked.connect(self._on_update_button_clicked)
        self.update_button.setVisible(False)  # 초기에는 숨김
        button_layout.addWidget(self.update_button)
        
        # 초기화 버튼
        self.clear_button = PushButton("초기화")
        self.clear_button.clicked.connect(self._on_clear_button_clicked)
        button_layout.addWidget(self.clear_button)
        
        # 조회 버튼
        self.search_button = PushButton("조회")
        self.search_button.clicked.connect(self._on_search_button_clicked)
        button_layout.addWidget(self.search_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def _connect_signals(self) -> None:
        """
        시그널 연결
        """
        # 사업자등록번호 입력 시 자동 조회 및 포맷 변환
        self.business_number_input.textChanged.connect(self._on_business_number_changed)
    
    def _on_business_number_changed(self, text: str) -> None:
        """
        사업자등록번호 입력 변경 시 자동 포맷 변환 및 조회
        
        Args:
            text: 입력된 사업자등록번호
        """
        # 하이픈 제거한 순수 숫자만 추출
        clean_text = text.replace('-', '')
        
        # 숫자만 입력되도록 제한
        if not clean_text.isdigit():
            return
        
        # 10자리를 초과하면 입력 제한
        if len(clean_text) > 10:
            # 마지막 입력을 제거
            self.business_number_input.textChanged.disconnect()
            self.business_number_input.setText(clean_text[:10])
            self.business_number_input.textChanged.connect(self._on_business_number_changed)
            return
        
        # 10자리 숫자가 입력되면 자동 포맷 변환
        if len(clean_text) == 10:
            formatted_text = self.business_service.format_business_number(clean_text)
            
            # 포맷 변환이 일어났다면 입력 필드 업데이트
            if formatted_text != text:
                # 시그널 연결을 일시적으로 해제하여 무한 루프 방지
                self.business_number_input.textChanged.disconnect()
                self.business_number_input.setText(formatted_text)
                self.business_number_input.textChanged.connect(self._on_business_number_changed)
    
    def _load_business_info_safe(self, business_number: str) -> None:
        """
        사업장 정보 안전 조회 (폼 초기화 없음)
        
        Args:
            business_number: 사업자등록번호
        """
        try:
            business_info = self.business_service.get_business_info(business_number)
            if business_info:
                # 기존 데이터가 있으면 폼에 채우기
                self._populate_form(business_info)
                self.current_business_number = business_number
                self.register_button.setVisible(False)
                self.update_button.setVisible(True)
                
                InfoBar.info(
                    title="정보",
                    content="기존 사업장 정보를 불러왔습니다.",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
            else:
                # 기존 데이터가 없으면 폼 초기화하지 않고 등록 모드로 설정
                self.current_business_number = None
                self.register_button.setVisible(True)
                self.update_button.setVisible(False)
                
                InfoBar.info(
                    title="정보",
                    content="새로운 사업장 정보를 등록할 수 있습니다.",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        except Exception as e:
            InfoBar.error(
                title="오류",
                content=f"사업장 정보 조회 중 오류가 발생했습니다: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self
            )
    
    def _load_business_info(self, business_number: str) -> None:
        """
        사업장 정보 로드 (조회 버튼용 - 폼 초기화 포함)
        
        Args:
            business_number: 사업자등록번호
        """
        try:
            business_info = self.business_service.get_business_info(business_number)
            if business_info:
                self._populate_form(business_info)
                self.current_business_number = business_number
                self.register_button.setVisible(False)
                self.update_button.setVisible(True)
                
                InfoBar.info(
                    title="정보",
                    content="기존 사업장 정보를 불러왔습니다.",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
            else:
                # 조회 버튼을 통한 조회 시에는 폼 초기화
                self._clear_form()
                self.current_business_number = None
                self.register_button.setVisible(True)
                self.update_button.setVisible(False)
                
                InfoBar.warning(
                    title="조회 결과",
                    content="해당 사업자등록번호로 등록된 정보가 없습니다.",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        except Exception as e:
            InfoBar.error(
                title="오류",
                content=f"사업장 정보 조회 중 오류가 발생했습니다: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self
            )
    
    def _populate_form(self, business_info: Dict[str, Any]) -> None:
        """
        폼에 사업장 정보 채우기
        
        Args:
            business_info: 사업장 정보 딕셔너리
        """
        self.business_number_input.setText(business_info.get('business_number', ''))
        self.business_name_input.setText(business_info.get('business_name', ''))
        self.owner_name_input.setText(business_info.get('owner_name', ''))
        self.owner_resident_number_input.setText(business_info.get('owner_resident_number', ''))
        self.business_type_input.setText(business_info.get('business_type', ''))
        self.business_category_input.setText(business_info.get('business_category', ''))
        self.address_input.setPlainText(business_info.get('address', ''))
        self.phone_number_input.setText(business_info.get('phone_number', ''))
        self.email_input.setText(business_info.get('email', ''))
    
    def _get_form_data(self) -> Dict[str, Any]:
        """
        폼에서 데이터 가져오기
        
        Returns:
            폼 데이터 딕셔너리
        """
        return {
            'business_number': self.business_number_input.text().strip(),
            'business_name': self.business_name_input.text().strip(),
            'owner_name': self.owner_name_input.text().strip(),
            'owner_resident_number': self.owner_resident_number_input.text().strip(),
            'business_type': self.business_type_input.text().strip(),
            'business_category': self.business_category_input.text().strip(),
            'address': self.address_input.toPlainText().strip(),
            'phone_number': self.phone_number_input.text().strip(),
            'email': self.email_input.text().strip()
        }
    
    def _validate_form_data(self, data: Dict[str, Any]) -> bool:
        """
        폼 데이터 유효성 검사
        
        Args:
            data: 검사할 데이터
            
        Returns:
            유효성 검사 결과
        """
        # 필수 필드 검사
        required_fields = ['business_number', 'business_name', 'owner_name']
        for field in required_fields:
            if not data[field]:
                InfoBar.warning(
                    title="입력 오류",
                    content=f"{field}은(는) 필수 입력 항목입니다.",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                return False
        
        # 사업자등록번호 형식 검사 (간단한 검사)
        business_number = data['business_number'].replace('-', '')
        if not business_number.isdigit() or len(business_number) != 10:
            InfoBar.warning(
                title="입력 오류",
                content="사업자등록번호는 10자리 숫자여야 합니다.",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return False
        
        # 이메일 형식 검사 (간단한 검사)
        email = data['email']
        if email and '@' not in email:
            InfoBar.warning(
                title="입력 오류",
                content="올바른 이메일 형식을 입력하세요.",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return False
        
        return True
    
    def _on_register_button_clicked(self) -> None:
        """
        등록 버튼 클릭 이벤트 처리
        """
        data = self._get_form_data()
        
        if not self._validate_form_data(data):
            return
        
        try:
            # 사업자등록번호에서 하이픈 제거
            data['business_number'] = data['business_number'].replace('-', '')
            
            self.business_service.create_business_info(data)
            
            InfoBar.success(
                title="등록 완료",
                content="사업장 정보가 성공적으로 등록되었습니다.",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            
            self.data_changed.emit()
            
        except Exception as e:
            InfoBar.error(
                title="등록 오류",
                content=f"사업장 정보 등록 중 오류가 발생했습니다: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self
            )
    
    def _on_update_button_clicked(self) -> None:
        """
        수정 버튼 클릭 이벤트 처리
        """
        if not self.current_business_number:
            return
        
        data = self._get_form_data()
        
        if not self._validate_form_data(data):
            return
        
        try:
            # 사업자등록번호에서 하이픈 제거
            data['business_number'] = data['business_number'].replace('-', '')
            
            self.business_service.update_business_info(self.current_business_number, data)
            
            InfoBar.success(
                title="수정 완료",
                content="사업장 정보가 성공적으로 수정되었습니다.",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            
            self.data_changed.emit()
            
        except Exception as e:
            InfoBar.error(
                title="수정 오류",
                content=f"사업장 정보 수정 중 오류가 발생했습니다: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self
            )
    
    def _on_clear_button_clicked(self) -> None:
        """
        초기화 버튼 클릭 이벤트 처리
        """
        self._clear_form()
        self.current_business_number = None
        self.register_button.setVisible(True)
        self.update_button.setVisible(False)
    
    def _on_search_button_clicked(self) -> None:
        """
        조회 버튼 클릭 이벤트 처리
        """
        business_number = self.business_number_input.text().strip()
        if business_number:
            # 하이픈 제거하고 DB 조회
            clean_business_number = business_number.replace('-', '')
            self._load_business_info(clean_business_number)
        else:
            InfoBar.warning(
                title="조회 오류",
                content="사업자등록번호를 입력하세요.",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
    
    def _clear_form(self) -> None:
        """
        폼 초기화
        """
        self.business_number_input.clear()
        self.business_name_input.clear()
        self.owner_name_input.clear()
        self.owner_resident_number_input.clear()
        self.business_type_input.clear()
        self.business_category_input.clear()
        self.address_input.clear()
        self.phone_number_input.clear()
        self.email_input.clear()
