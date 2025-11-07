"""
거래처정보 등록 인터페이스

거래처정보를 등록하고 관리하는 페이지를 구현합니다.
"""

from typing import Optional, Dict, Any, List
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (
  QWidget, 
  QVBoxLayout, 
  QHBoxLayout, 
  QFormLayout,
  QGridLayout,
  QHeaderView,
  QAbstractItemView,
  QSpacerItem,
  QSizePolicy
)
from qfluentwidgets import (
  PrimaryPushButton,
  PushButton,
  LineEdit,
  InfoBar,
  InfoBarPosition,
  CardWidget,
  TitleLabel,
  BodyLabel,
  ComboBox,
  TableView,
  DateEdit,
  FastCalendarPicker,
  FluentIcon
)
from PySide6.QtCore import QDate
from app.services.vendor_service import VendorService
from app.services.common_code_service import CommonCodeService
from app.models.vendor_model import VendorModel


class VendorInterface(QWidget):
  """
  거래처정보 등록 인터페이스
  
  거래처정보를 등록하고 관리하는 페이지입니다.
  """
  
  # 데이터 변경 시그널
  data_changed = Signal()
  
  def __init__(self):
    super().__init__()
    self.vendor_service = VendorService()
    self.common_code_service = CommonCodeService()
    self.current_vendor_id: Optional[int] = None
    self._init_ui()
    self._connect_signals()
    self._load_common_codes()
  
  def _init_ui(self) -> None:
    """
    거래처정보 등록 인터페이스 UI 초기화
    """
    layout = QVBoxLayout(self)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)
    
    # 제목/버튼 섹션
    title_layout = QHBoxLayout()
    # 제목
    title_label = TitleLabel("거래처정보 관리")
    title_layout.addWidget(title_label)
    title_layout.addStretch()
    # 버튼 섹션
    button_layout = QHBoxLayout()
    button_layout.setSpacing(10)
    # 조회 버튼
    self.search_button: PushButton = PrimaryPushButton("조회", icon=FluentIcon.SEARCH)
    self.search_button.setMinimumWidth(100)
    self.search_button.setMaximumWidth(100)
    button_layout.addWidget(self.search_button)
    # 신규 버튼
    self.new_button: PushButton = PrimaryPushButton("신규", icon=FluentIcon.ADD)
    self.new_button.setMinimumWidth(100)
    self.new_button.setMaximumWidth(100)
    button_layout.addWidget(self.new_button)
    # 저장 버튼
    self.save_button: PushButton = PrimaryPushButton("저장", icon=FluentIcon.SAVE)
    self.save_button.setMinimumWidth(100)
    self.save_button.setMaximumWidth(100)
    button_layout.addWidget(self.save_button)
    # 삭제 버튼
    self.delete_button: PushButton = PrimaryPushButton("삭제", icon=FluentIcon.DELETE)
    self.delete_button.setMinimumWidth(100)
    self.delete_button.setMaximumWidth(100)
    button_layout.addWidget(self.delete_button)
    # 초기화 버튼
    self.reset_button: PushButton = PrimaryPushButton("초기화", icon=FluentIcon.ROTATE)
    self.reset_button.setMinimumWidth(100)
    self.reset_button.setMaximumWidth(100)
    button_layout.addWidget(self.reset_button)

    title_layout.addLayout(button_layout)

    layout.addLayout(title_layout)
    
    # 검색조건 섹션
    search_card = CardWidget()
    search_card.setFixedHeight(80)
    search_layout = QHBoxLayout(search_card)
    search_layout.setSpacing(15)
    search_layout.setContentsMargins(20, 20, 20, 20)
    
    # 검색조건: 사업자등록번호
    business_number_label = BodyLabel("사업자등록번호:")
    business_number_label.setMinimumWidth(120)
    business_number_label.setMaximumWidth(120)
    search_layout.addWidget(business_number_label)
    self.search_business_number_input: LineEdit = LineEdit()
    self.search_business_number_input.setPlaceholderText("사업자등록번호로 검색")
    # 사업자등록번호 입력 필드 기본 폭 설정
    self.search_business_number_input.setMinimumWidth(220)
    self.search_business_number_input.setMaximumWidth(220)
    search_layout.addWidget(self.search_business_number_input)
    
    # 검색조건: 거래처명
    search_layout.addSpacing(30)  # 간격 추가
    vendor_name_label = BodyLabel("거래처명:")
    vendor_name_label.setMinimumWidth(120)
    vendor_name_label.setMaximumWidth(120)
    search_layout.addWidget(vendor_name_label)
    self.search_vendor_name_input: LineEdit = LineEdit()
    self.search_vendor_name_input.setPlaceholderText("거래처명으로 검색")
    # 사업자거래처명등록번호 입력 필드 기본 폭 설정
    self.search_vendor_name_input.setMinimumWidth(330)
    self.search_vendor_name_input.setMaximumWidth(450)
    search_layout.addWidget(self.search_vendor_name_input)
    search_layout.addStretch()

    layout.addWidget(search_card)
    
    # 거래처정보 등록 섹션과 버튼 영역을 담을 수평 레이아웃
    main_content_layout = QHBoxLayout()
    main_content_layout.setSpacing(20)
    
    # 거래처정보 등록 폼 카드
    form_card = CardWidget()
    form_card_layout = QGridLayout(form_card)
    form_card_layout.setContentsMargins(20, 20, 20, 20)
    form_card_layout.setHorizontalSpacing(20)  # 컬럼 간 가로 간격 고정
    form_card_layout.setVerticalSpacing(10)  # 행 간격
    form_card_layout.setColumnMinimumWidth(2, 20)  # 두 번째 열(빈 칸) 간격 고정
    form_card_layout.setColumnMinimumWidth(5, 20)  # 다섯 번째 열(빈 칸) 간격 고정
    
    # 첫 번째 줄 (row=0): 사업자등록번호, 거래처명
    row = 0
    
    # 사업자등록번호
    business_number_label = BodyLabel("사업자등록번호 *")
    business_number_label.setMinimumWidth(120)
    business_number_label.setMaximumWidth(120)
    form_card_layout.addWidget(business_number_label, row, 0)
    self.business_number_input: LineEdit = LineEdit()
    self.business_number_input.setPlaceholderText("사업자등록번호를 입력하세요")
    # 자동 포맷팅을 위해 maxLength를 12로 설정 (xxx-xx-xxxxx = 12자리)
    self.business_number_input.setMaxLength(12)
    # 사업자등록번호 입력 필드 기본 폭 설정
    self.business_number_input.setMinimumWidth(220)
    self.business_number_input.setMaximumWidth(220)
    form_card_layout.addWidget(self.business_number_input, row, 1)
    
    # 빈 칸 추가
    form_card_layout.addItem(QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Fixed), row, 2)
    
    # 거래처명
    # form_card_layout.setSpacing(30)  # 간격 추가
    vendor_name_label = BodyLabel("거래처명 *")
    vendor_name_label.setMinimumWidth(120)
    vendor_name_label.setMaximumWidth(120)
    form_card_layout.addWidget(vendor_name_label, row, 3)
    self.vendor_name_input: LineEdit = LineEdit()
    self.vendor_name_input.setPlaceholderText("거래처명을 입력하세요")
    self.vendor_name_input.setMaxLength(255)
    form_card_layout.addWidget(self.vendor_name_input, row, 4, 1, 3)  # 4번 열부터 3개 열 차지 (4, 5, 6)
    
    # 두 번째 줄 (row=1): 과세유형, 사업자 상태, 상태 업데이트일
    row = 1
    
    # 과세유형
    tax_type_label = BodyLabel("과세유형")
    tax_type_label.setMinimumWidth(120)
    tax_type_label.setMaximumWidth(120)
    form_card_layout.addWidget(tax_type_label, row, 0)
    self.tax_type_combo: ComboBox = ComboBox()
    self.tax_type_combo.setPlaceholderText("과세유형을 선택하세요")
    # 과세유형 입력 필드 기본 폭 설정
    self.tax_type_combo.setMinimumWidth(220)
    self.tax_type_combo.setMaximumWidth(220)
    form_card_layout.addWidget(self.tax_type_combo, row, 1)
    
    # 빈 칸 추가
    form_card_layout.addItem(QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Fixed), row, 2)
    
    # 사업자 상태
    # form_card_layout.setSpacing(30)  # 간격 추가
    business_status_label = BodyLabel("사업자 상태")
    business_status_label.setMinimumWidth(120)
    business_status_label.setMaximumWidth(120)
    form_card_layout.addWidget(business_status_label, row, 3)
    self.business_status_combo: ComboBox = ComboBox()
    self.business_status_combo.setPlaceholderText("사업자 상태를 선택하세요")
    # 사업자 상태 입력 필드 기본 폭 설정
    self.business_status_combo.setMinimumWidth(220)
    self.business_status_combo.setMaximumWidth(220)
    form_card_layout.addWidget(self.business_status_combo, row, 4)
    
    # 빈 칸 추가
    form_card_layout.addItem(QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Fixed), row, 5)
    
    # 상태 업데이트일
    # form_card_layout.setSpacing(30)  # 간격 추가
    status_updated_label = BodyLabel("상태 업데이트일")
    status_updated_label.setMinimumWidth(120)
    status_updated_label.setMaximumWidth(120)
    form_card_layout.addWidget(status_updated_label, row, 6)
    # FastCalendarPicker: 빠른 캘린더 선택 위젯
    self.status_updated_at_input: FastCalendarPicker = FastCalendarPicker()
    self.status_updated_at_input.setDate(QDate.currentDate())  # 현재 날짜로 초기화
    form_card_layout.addWidget(self.status_updated_at_input, row, 7)
    
    # 컬럼 스트레치 비율 설정
    form_card_layout.setColumnStretch(0, 0)  # 사업자등록번호 라벨 (고정)
    form_card_layout.setColumnStretch(1, 0)  # 사업자등록번호 입력 (고정)
    form_card_layout.setColumnStretch(2, 0)  # 빈 칸 (고정 너비)
    form_card_layout.setColumnStretch(3, 0)  # 거래처명 라벨 (고정)
    form_card_layout.setColumnStretch(4, 1)  # 거래처명 입력 (확장)
    form_card_layout.setColumnStretch(5, 0)  # 빈 칸 (고정 너비)
    form_card_layout.setColumnStretch(6, 0)  # 상태 업데이트일 라벨 (고정)
    form_card_layout.setColumnStretch(7, 0)  # 상태 업데이트일 입력 (고정)
    
    main_content_layout.addWidget(form_card)
    
    layout.addLayout(main_content_layout)
    
    # 거래처정보 목록 섹션
    list_card = CardWidget()
    list_layout = QVBoxLayout(list_card)
    list_layout.setContentsMargins(20, 20, 20, 20)
    list_layout.setSpacing(10)
    
    # 목록 제목
    list_title = BodyLabel("거래처정보 목록")
    list_title.setStyleSheet("font-weight: bold; font-size: 14px;")
    list_layout.addWidget(list_title)
    
    # 테이블 뷰 (QFluentWidgets의 TableView 사용)
    self.vendor_table_view: TableView = TableView()
    self.vendor_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.vendor_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.vendor_table_view.setAlternatingRowColors(True)
    self.vendor_table_view.setSortingEnabled(True)
    
    # 테이블 뷰 폰트 설정 (맑은 고딕)
    font_db = QFontDatabase()
    available_fonts = font_db.families()
    font_family = "맑은 고딕"
    if font_family not in available_fonts:
        font_family = "Malgun Gothic"
        if font_family not in available_fonts:
            font_family = QFont().family()
    table_font = QFont(font_family)
    table_font.setPointSize(9)
    self.vendor_table_view.setFont(table_font)
    # 헤더 폰트도 설정
    header = self.vendor_table_view.horizontalHeader()
    header.setFont(table_font)
    
    # 스타일시트를 통한 폰트 강제 적용 (FluentWidgets TableView용)
    self.vendor_table_view.setStyleSheet(f"""
        QTableView {{
            font-family: "{font_family}", "Malgun Gothic", "맑은 고딕", sans-serif;
            font-size: 9pt;
        }}
        QHeaderView::section {{
            font-family: "{font_family}", "Malgun Gothic", "맑은 고딕", sans-serif;
            font-size: 9pt;
        }}
    """)
    
    # 테이블 모델 설정
    self.vendor_model = VendorModel(self)
    self.vendor_table_view.setModel(self.vendor_model)
    
    # 컬럼 너비 자동 조절
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    list_layout.addWidget(self.vendor_table_view)
    
    # 테이블 선택 시 상세 정보를 폼에 표시
    self.vendor_table_view.selectionModel().selectionChanged.connect(
      self._on_table_selection_changed
    )
    
    layout.addWidget(list_card)
    layout.addStretch()
  
  def _connect_signals(self) -> None:
    """
    시그널 연결
    """
    # 사업자등록번호 입력 시 자동 포맷팅
    self.search_business_number_input.textChanged.connect(self._on_search_business_number_changed)
    self.business_number_input.textChanged.connect(self._on_business_number_changed)
    
    # 버튼 클릭 이벤트
    self.search_button.clicked.connect(self._on_search_button_clicked)
    self.new_button.clicked.connect(self._on_new_button_clicked)
    self.save_button.clicked.connect(self._on_save_button_clicked)
    self.delete_button.clicked.connect(self._on_delete_button_clicked)
    self.reset_button.clicked.connect(self._on_reset_button_clicked)
  
  def _format_business_number(self, text: str) -> str:
    """
    사업자등록번호를 xxx-xx-xxxxx 형식으로 포맷팅
    
    Args:
      text: 입력된 사업자등록번호 (하이픈 포함 또는 제외)
    
    Returns:
      xxx-xx-xxxxx 형식으로 포맷팅된 사업자등록번호
    """
    # 하이픈 제거한 순수 숫자만 추출
    clean_text = text.replace('-', '')
    
    # 숫자가 아니면 빈 문자열 반환
    if not clean_text.isdigit():
      return ''
    
    # 10자리를 초과하면 10자리로 제한
    if len(clean_text) > 10:
      clean_text = clean_text[:10]
    
    # 자동 포맷팅: xxx-xx-xxxxx
    if len(clean_text) == 10:
      return f"{clean_text[:3]}-{clean_text[3:5]}-{clean_text[5:]}"
    elif len(clean_text) > 5:  # 7자리 이상: xxx-xx-xxxxx
      return f"{clean_text[:3]}-{clean_text[3:5]}-{clean_text[5:]}"
    elif len(clean_text) > 3:  # 4-6자리: xxx-xx
      return f"{clean_text[:3]}-{clean_text[3:]}"
    else:  # 3자리 이하
      return clean_text
  
  def _clean_business_number(self, text: str) -> str:
    """
    사업자등록번호에서 하이픈을 제거한 10자리 숫자 반환
    
    Args:
      text: 사업자등록번호 (하이픈 포함 가능)
    
    Returns:
      하이픈이 제거된 10자리 숫자 문자열
    """
    # 하이픈 제거한 순수 숫자만 추출
    clean_text = text.replace('-', '')
    
    # 숫자만 반환 (최대 10자리)
    if clean_text.isdigit():
      return clean_text[:10]
    
    return ''
  
  def _on_search_business_number_changed(self, text: str) -> None:
    """
    검색조건 사업자등록번호 입력 변경 시 자동 포맷 변환 (xxx-xx-xxxxx)
    
    Args:
      text: 입력된 사업자등록번호
    """
    formatted_text = self._format_business_number(text)
    
    # 포맷 변환이 일어났다면 입력 필드 업데이트
    if formatted_text != text:
      # 시그널 연결을 일시적으로 해제하여 무한 루프 방지
      self.search_business_number_input.textChanged.disconnect()
      self.search_business_number_input.setText(formatted_text)
      self.search_business_number_input.textChanged.connect(self._on_search_business_number_changed)
  
  def _on_business_number_changed(self, text: str) -> None:
    """
    등록 폼 사업자등록번호 입력 변경 시 자동 포맷 변환 (xxx-xx-xxxxx)
    
    Args:
      text: 입력된 사업자등록번호
    """
    formatted_text = self._format_business_number(text)
    
    # 포맷 변환이 일어났다면 입력 필드 업데이트
    if formatted_text != text:
      # 시그널 연결을 일시적으로 해제하여 무한 루프 방지
      self.business_number_input.textChanged.disconnect()
      self.business_number_input.setText(formatted_text)
      self.business_number_input.textChanged.connect(self._on_business_number_changed)
  
  def _load_common_codes(self) -> None:
    """
    공통코드 목록 로드 (과세유형, 사업자 상태)
    
    code_group이 "tax_type", "business_status"인 코드를 로드하여
    코드약어(code_abbr)를 표시하고, 선택 시 코드값(code)이 저장되도록 설정합니다.
    """
    try:
      # 과세유형 코드 로드 (code_group: "tax_type")
      tax_types = self.common_code_service.get_common_codes_by_group('tax_type')
      self.tax_type_combo.clear()
      self.tax_type_combo.addItem("선택", userData=None)
      for tax_type in tax_types:
        if tax_type.get('is_active', True):
          code = tax_type.get('code', '')
          code_abbr = tax_type.get('code_abbr', '')
          # 코드약어를 표시하고, 코드값을 userData로 저장
          self.tax_type_combo.addItem(code_abbr, userData=code)
      
      # 사업자 상태 코드 로드 (code_group: "business_status")
      business_statuses = self.common_code_service.get_common_codes_by_group('business_status')
      self.business_status_combo.clear()
      self.business_status_combo.addItem("선택", userData=None)
      for business_status in business_statuses:
        if business_status.get('is_active', True):
          code = business_status.get('code', '')
          code_abbr = business_status.get('code_abbr', '')
          # 코드약어를 표시하고, 코드값을 userData로 저장
          self.business_status_combo.addItem(code_abbr, userData=code)
      
    except Exception as e:
      InfoBar.warning(
        title="경고",
        content=f"공통코드 목록을 불러오는 중 오류가 발생했습니다: {str(e)}",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
  
  def _on_search_button_clicked(self) -> None:
    """
    조회 버튼 클릭 이벤트 처리
    """
    try:
      # 검색조건 가져오기
      business_number = self.search_business_number_input.text().strip()
      vendor_name = self.search_vendor_name_input.text().strip()
      
      # 검색 파라미터 설정
      search_params = {}
      if business_number:
        # 사업자등록번호에서 "-"를 제거한 값으로 DB 조회
        clean_business_number = self._clean_business_number(business_number)
        if clean_business_number:
          search_params['business_number'] = clean_business_number
      if vendor_name:
        search_params['vendor_name'] = vendor_name
      
      # 검색 실행
      results = self.vendor_service.search_vendors(**search_params)
      
      # 테이블 모델에 데이터 설정
      self.vendor_model.set_data(results)
      
      # 조회 결과 메시지
      InfoBar.success(
        title="조회 완료",
        content=f"총 {len(results)}건의 거래처정보를 찾았습니다.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      
    except Exception as e:
      InfoBar.error(
        title="조회 오류",
        content=f"거래처정보 조회 중 오류가 발생했습니다: {str(e)}",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=self
      )
  
  def _on_new_button_clicked(self) -> None:
    """
    신규 버튼 클릭 이벤트 처리
    """
    self._clear_form()
    self.current_vendor_id = None
    # 테이블 선택 해제
    self.vendor_table_view.clearSelection()
  
  def _on_save_button_clicked(self) -> None:
    """
    저장 버튼 클릭 이벤트 처리
    """
    data = self._get_form_data()
    
    if not self._validate_form_data(data):
      return
    
    try:
      vendor_data = {
        'business_number': data['business_number'],
        'vendor_name': data['vendor_name'],
        'tax_type': data.get('tax_type') or None,
        'business_status': data.get('business_status') or None,
        'status_updated_at': data.get('status_updated_at') or None
      }
      
      if self.current_vendor_id:
        # 수정 모드
        updated = self.vendor_service.update_vendor(
          self.current_vendor_id,
          vendor_data
        )
        
        if updated:
          InfoBar.success(
            title="수정 완료",
            content="거래처정보가 성공적으로 수정되었습니다.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
          )
      else:
        # 등록 모드
        created = self.vendor_service.create_vendor(
          vendor_data
        )
        
        if created:
          InfoBar.success(
            title="등록 완료",
            content="거래처정보가 성공적으로 등록되었습니다.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
          )
      
      # 조회 버튼 클릭하여 목록 갱신
      self._on_search_button_clicked()
      
      # 폼 초기화
      self._on_new_button_clicked()
      
      self.data_changed.emit()
      
    except ValueError as e:
      InfoBar.warning(
        title="입력 오류",
        content=str(e),
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
    except Exception as e:
      InfoBar.error(
        title="저장 오류",
        content=f"거래처정보 저장 중 오류가 발생했습니다: {str(e)}",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=self
      )
  
  def _on_delete_button_clicked(self) -> None:
    """
    삭제 버튼 클릭 이벤트 처리
    """
    if not self.current_vendor_id:
      InfoBar.warning(
        title="삭제 오류",
        content="삭제할 거래처정보를 선택해주세요.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      return
    
    try:
      deleted = self.vendor_service.delete_vendor(
        self.current_vendor_id
      )
      
      if deleted:
        InfoBar.success(
          title="삭제 완료",
          content="거래처정보가 성공적으로 삭제되었습니다.",
          orient=Qt.Horizontal,
          isClosable=True,
          position=InfoBarPosition.TOP,
          duration=1000,
          parent=self
        )
        
        # 조회 버튼 클릭하여 목록 갱신
        self._on_search_button_clicked()
        
        # 폼 초기화
        self._on_new_button_clicked()
        
        self.data_changed.emit()
      else:
        InfoBar.warning(
          title="삭제 오류",
          content="거래처정보 삭제에 실패했습니다.",
          orient=Qt.Horizontal,
          isClosable=True,
          position=InfoBarPosition.TOP,
          duration=1000,
          parent=self
        )
        
    except Exception as e:
      InfoBar.error(
        title="삭제 오류",
        content=f"거래처정보 삭제 중 오류가 발생했습니다: {str(e)}",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=self
      )
  
  def _on_reset_button_clicked(self) -> None:
    """
    초기화 버튼 클릭 이벤트 처리
    """
    self._clear_form()
    self.current_vendor_id = None
    self.vendor_table_view.clearSelection()
    self.search_business_number_input.clear()
    self.search_vendor_name_input.clear()
    self.vendor_model.clear()
  
  def _on_table_selection_changed(self) -> None:
    """
    테이블 선택 변경 이벤트 처리
    """
    selected_indexes = self.vendor_table_view.selectionModel().selectedRows()
    
    if not selected_indexes:
      return
    
    # 첫 번째 선택된 행 가져오기
    row = selected_indexes[0].row()
    vendor_data = self.vendor_model.get_row_data(row)
    
    if vendor_data:
      self._populate_form(vendor_data)
      self.current_vendor_id = vendor_data.get('id')
  
  def _populate_form(self, vendor_data: Dict[str, Any]) -> None:
    """
    폼에 거래처정보 채우기
    
    Args:
      vendor_data: 거래처정보 딕셔너리
    """
    # 사업자등록번호 (xxx-xx-xxxxx 형식으로 표시)
    business_number = vendor_data.get('business_number', '')
    if business_number:
      formatted_business_number = self._format_business_number(business_number)
      self.business_number_input.setText(formatted_business_number)
    else:
      self.business_number_input.clear()
    
    # 거래처명
    self.vendor_name_input.setText(vendor_data.get('vendor_name', ''))
    
    # 과세유형 선택
    tax_type = vendor_data.get('tax_type')
    if tax_type:
      for i in range(1, self.tax_type_combo.count()):  # 인덱스 0은 "선택"
        if self.tax_type_combo.itemData(i) == tax_type:
          self.tax_type_combo.setCurrentIndex(i)
          break
    else:
      self.tax_type_combo.setCurrentIndex(0)
    
    # 사업자 상태 선택
    business_status = vendor_data.get('business_status')
    if business_status:
      for i in range(1, self.business_status_combo.count()):  # 인덱스 0은 "선택"
        if self.business_status_combo.itemData(i) == business_status:
          self.business_status_combo.setCurrentIndex(i)
          break
    else:
      self.business_status_combo.setCurrentIndex(0)
    
    # 상태 업데이트 날짜
    status_updated_at = vendor_data.get('status_updated_at')
    if status_updated_at:
      try:
        if isinstance(status_updated_at, str):
          from datetime import datetime
          date = datetime.fromisoformat(status_updated_at.replace('Z', '+00:00'))
          self.status_updated_at_input.setDate(QDate(date.year, date.month, date.day))
        else:
          self.status_updated_at_input.setDate(QDate.currentDate())
      except:
        self.status_updated_at_input.setDate(QDate.currentDate())
    else:
      self.status_updated_at_input.setDate(QDate.currentDate())
  
  def _get_form_data(self) -> Dict[str, Any]:
    """
    폼에서 데이터 가져오기
    
    Returns:
      폼 데이터 딕셔너리
    """
    # 과세유형 코드 가져오기 (인덱스 0이면 "선택"이므로 None)
    tax_type = None
    current_index = self.tax_type_combo.currentIndex()
    if current_index > 0:
      tax_type = self.tax_type_combo.currentData()
    
    # 사업자 상태 코드 가져오기 (인덱스 0이면 "선택"이므로 None)
    business_status = None
    current_index = self.business_status_combo.currentIndex()
    if current_index > 0:
      business_status = self.business_status_combo.currentData()
    
    # 상태 업데이트 날짜
    date = self.status_updated_at_input.date()
    status_updated_at = date.toPython().isoformat() if date.isValid() else None
    
    # 사업자등록번호에서 "-"를 제거한 값으로 저장
    business_number = self.business_number_input.text().strip()
    clean_business_number = self._clean_business_number(business_number)
    
    return {
      'business_number': clean_business_number,
      'vendor_name': self.vendor_name_input.text().strip(),
      'tax_type': tax_type,
      'business_status': business_status,
      'status_updated_at': status_updated_at
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
    required_fields = {
      'business_number': '사업자등록번호',
      'vendor_name': '거래처명'
    }
    
    for field, field_name in required_fields.items():
      if not data.get(field):
        InfoBar.warning(
          title="입력 오류",
          content=f"{field_name}은(는) 필수 입력 항목입니다.",
          orient=Qt.Horizontal,
          isClosable=True,
          position=InfoBarPosition.TOP,
          duration=1000,
          parent=self
        )
        return False
    
    # 사업자등록번호 형식 검사 (10자리 숫자)
    business_number = data.get('business_number', '')
    clean_business_number = self._clean_business_number(business_number)
    if len(clean_business_number) != 10 or not clean_business_number.isdigit():
      InfoBar.warning(
        title="입력 오류",
        content="사업자등록번호는 10자리 숫자여야 합니다.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      return False
    
    return True
  
  def _clear_form(self) -> None:
    """
    폼 초기화
    """
    self.business_number_input.clear()
    self.vendor_name_input.clear()
    self.tax_type_combo.setCurrentIndex(0)
    self.business_status_combo.setCurrentIndex(0)
    self.status_updated_at_input.setDate(QDate.currentDate())

