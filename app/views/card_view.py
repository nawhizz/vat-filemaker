"""
카드 정보 등록 인터페이스

카드 정보를 등록하고 관리하는 페이지를 구현합니다.
"""

from typing import Optional, Dict, Any, List
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
  QWidget, 
  QVBoxLayout, 
  QHBoxLayout, 
  QFormLayout,
  QHeaderView,
  QAbstractItemView
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
  CheckBox,
  FluentIcon
)
from app.services.card_service import CardService
from app.services.card_company_service import CardCompanyService
from app.models.card_model import CardModel


class CardInterface(QWidget):
  """
  카드 정보 등록 인터페이스
  
  카드 정보를 등록하고 관리하는 페이지입니다.
  """
  
  # 데이터 변경 시그널
  data_changed = Signal()
  
  def __init__(self):
    super().__init__()
    self.card_service = CardService()
    self.card_company_service = CardCompanyService()
    self.current_card_id: Optional[int] = None
    self._init_ui()
    self._connect_signals()
    self._load_card_companies()
  
  def _init_ui(self) -> None:
    """
    카드 정보 등록 인터페이스 UI 초기화
    """
    layout = QVBoxLayout(self)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)
    
    # 제목
    title_label = TitleLabel("카드 정보 관리")
    layout.addWidget(title_label)
    
    # 설명
    # description_label = BodyLabel("카드 정보를 등록하고 관리할 수 있습니다.")
    # layout.addWidget(description_label)
    
    # 검색조건 섹션
    search_card = CardWidget()
    search_card.setFixedHeight(80)
    search_layout = QHBoxLayout(search_card)
    search_layout.setSpacing(15)
    search_layout.setContentsMargins(20, 20, 20, 20)

    # 검색조건: 카드사 선택
    card_company_label = BodyLabel("카드사:")
    search_layout.addWidget(card_company_label)
    self.search_card_company_combo: ComboBox = ComboBox()
    self.search_card_company_combo.setPlaceholderText("카드사 선택 (전체)")
    search_layout.addWidget(self.search_card_company_combo)

    # 검색조건: 카드명
    card_name_label = BodyLabel("카드명:")
    search_layout.addWidget(card_name_label)
    self.search_card_name_input: LineEdit = LineEdit()
    self.search_card_name_input.setPlaceholderText("카드명으로 검색")
    search_layout.addWidget(self.search_card_name_input)
    
    search_layout.addStretch()
    
    layout.addWidget(search_card)
    
    # 카드 정보 등록 섹션과 버튼 영역을 담을 수평 레이아웃
    main_content_layout = QHBoxLayout()
    main_content_layout.setSpacing(20)
    
    # 카드 정보 등록 폼 카드
    form_card = CardWidget()
    form_card.setFixedWidth(400)
    form_layout = QFormLayout(form_card)
    form_layout.setSpacing(15)
    form_layout.setContentsMargins(20, 20, 20, 20)
    
    # 카드번호
    self.card_number_input: LineEdit = LineEdit()
    self.card_number_input.setPlaceholderText("카드번호를 입력하세요")
    form_layout.addRow("카드번호 *", self.card_number_input)
    
    # 마스킹된 카드번호 (사용자 입력)
    self.masked_card_number_input: LineEdit = LineEdit()
    self.masked_card_number_input.setPlaceholderText("마스킹된 카드번호를 입력하세요 (예: 1234-****-****-5678)")
    self.masked_card_number_input.setMaxLength(50)
    form_layout.addRow("마스킹 카드번호 *", self.masked_card_number_input)
    
    # 카드명
    self.card_name_input: LineEdit = LineEdit()
    self.card_name_input.setPlaceholderText("카드명을 입력하세요")
    self.card_name_input.setMaxLength(255)
    form_layout.addRow("카드명 *", self.card_name_input)
    
    # 카드유형
    self.card_type_input: LineEdit = LineEdit()
    self.card_type_input.setPlaceholderText("카드유형을 입력하세요 (예: 체크카드, 신용카드)")
    self.card_type_input.setMaxLength(50)
    form_layout.addRow("카드유형", self.card_type_input)
    
    # 카드사 선택
    self.card_company_combo: ComboBox = ComboBox()
    self.card_company_combo.setPlaceholderText("카드사를 선택하세요")
    form_layout.addRow("카드사 *", self.card_company_combo)
    
    # 사용여부
    self.is_active_checkbox: CheckBox = CheckBox("사용")
    self.is_active_checkbox.setChecked(True)
    form_layout.addRow("사용여부", self.is_active_checkbox)
    
    main_content_layout.addWidget(form_card)
    
    # 버튼 영역
    button_layout = QVBoxLayout()
    button_layout.setSpacing(15)
    
    # 조회 버튼
    self.search_button: PrimaryPushButton = PrimaryPushButton("조회", icon=FluentIcon.SEARCH)
    button_layout.addWidget(self.search_button)
    
    # 신규 버튼
    self.new_button: PushButton = PrimaryPushButton("신규", icon=FluentIcon.ADD)
    button_layout.addWidget(self.new_button)
    
    # 저장 버튼
    self.save_button: PrimaryPushButton = PrimaryPushButton("저장", icon=FluentIcon.SAVE)
    button_layout.addWidget(self.save_button)
    
    # 초기화 버튼
    self.reset_button: PushButton = PrimaryPushButton("초기화", icon=FluentIcon.ROTATE)
    button_layout.addWidget(self.reset_button)
    
    button_layout.addStretch()
    main_content_layout.addLayout(button_layout)
    main_content_layout.addStretch()
    
    layout.addLayout(main_content_layout)
    
    # 카드 정보 목록 섹션
    list_card = CardWidget()
    list_layout = QVBoxLayout(list_card)
    list_layout.setContentsMargins(20, 20, 20, 20)
    list_layout.setSpacing(10)
    
    # 목록 제목
    list_title = BodyLabel("카드 정보 목록")
    list_title.setStyleSheet("font-weight: bold; font-size: 14px;")
    list_layout.addWidget(list_title)
    
    # 테이블 뷰 (QFluentWidgets의 TableView 사용)
    self.card_table_view: TableView = TableView()
    self.card_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.card_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.card_table_view.setAlternatingRowColors(True)
    self.card_table_view.setSortingEnabled(True)
    
    # 테이블 모델 설정
    self.card_model = CardModel(self)
    self.card_table_view.setModel(self.card_model)
    
    # 컬럼 너비 자동 조절
    header = self.card_table_view.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    list_layout.addWidget(self.card_table_view)
    
    # 테이블 선택 시 상세 정보를 폼에 표시
    self.card_table_view.selectionModel().selectionChanged.connect(
      self._on_table_selection_changed
    )
    
    layout.addWidget(list_card)
    layout.addStretch()
  
  def _connect_signals(self) -> None:
    """
    시그널 연결
    """
    # 버튼 클릭 이벤트
    self.search_button.clicked.connect(self._on_search_button_clicked)
    self.new_button.clicked.connect(self._on_new_button_clicked)
    self.save_button.clicked.connect(self._on_save_button_clicked)
    self.reset_button.clicked.connect(self._on_reset_button_clicked)
  
  def _load_card_companies(self) -> None:
    """
    카드사 목록 로드
    """
    try:
      card_companies = self.card_company_service.get_all_card_companies()
      
      # 검색 콤보박스에 "전체" 추가
      self.search_card_company_combo.clear()
      self.search_card_company_combo.addItem("전체", userData=None)
      
      # 등록 폼 콤보박스 초기화 및 "선택" 항목 추가
      self.card_company_combo.clear()
      self.card_company_combo.addItem("선택", userData=None)
      
      for company in card_companies:
        company_name = company.get('card_company_name', '')
        company_id = company.get('id')
        
        # 검색 콤보박스에 추가
        self.search_card_company_combo.addItem(company_name, userData=company_id)
        
        # 등록 폼 콤보박스에 추가
        self.card_company_combo.addItem(company_name, userData=company_id)
      
    except Exception as e:
      InfoBar.warning(
        title="경고",
        content=f"카드사 목록을 불러오는 중 오류가 발생했습니다: {str(e)}",
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
      card_name = self.search_card_name_input.text().strip()
      
      # 카드사 선택
      card_company_id = None
      current_index = self.search_card_company_combo.currentIndex()
      if current_index > 0:  # "전체"가 아닌 경우
        card_company_id = self.search_card_company_combo.currentData()
      
      # 검색 파라미터 설정
      search_params = {}
      if card_name:
        search_params['card_name'] = card_name
      if card_company_id is not None:
        search_params['card_company_id'] = card_company_id
      
      # 검색 실행
      results = self.card_service.search_cards(**search_params)
      
      # 테이블 모델에 데이터 설정
      self.card_model.set_data(results)
      
      # 조회 결과 메시지
      InfoBar.success(
        title="조회 완료",
        content=f"총 {len(results)}건의 카드 정보를 찾았습니다.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      
    except Exception as e:
      InfoBar.error(
        title="조회 오류",
        content=f"카드 정보 조회 중 오류가 발생했습니다: {str(e)}",
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
    self.current_card_id = None
    # 테이블 선택 해제
    self.card_table_view.clearSelection()
  
  def _on_save_button_clicked(self) -> None:
    """
    저장 버튼 클릭 이벤트 처리
    """
    data = self._get_form_data()
    
    if not self._validate_form_data(data):
      return
    
    try:
      card_data = {
        'card_number': data['card_number'],
        'masked_card_number': data['masked_card_number'],
        'card_name': data['card_name'],
        'card_type': data.get('card_type', '') or None,
        'card_company_id': data['card_company_id'],
        'is_active': data.get('is_active', True)
      }
      
      if self.current_card_id:
        # 수정 모드
        updated = self.card_service.update_card(
          self.current_card_id,
          card_data
        )
        
        if updated:
          InfoBar.success(
            title="수정 완료",
            content="카드 정보가 성공적으로 수정되었습니다.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
          )
      else:
        # 등록 모드
        created = self.card_service.create_card(
          card_data
        )
        
        if created:
          InfoBar.success(
            title="등록 완료",
            content="카드 정보가 성공적으로 등록되었습니다.",
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
        content=f"카드 정보 저장 중 오류가 발생했습니다: {str(e)}",
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
    self.current_card_id = None
    self.card_table_view.clearSelection()
    self.search_card_name_input.clear()
    self.search_card_company_combo.setCurrentIndex(0)
    self.card_model.clear()
  
  def _on_table_selection_changed(self) -> None:
    """
    테이블 선택 변경 이벤트 처리
    """
    selected_indexes = self.card_table_view.selectionModel().selectedRows()
    
    if not selected_indexes:
      return
    
    # 첫 번째 선택된 행 가져오기
    row = selected_indexes[0].row()
    card_data = self.card_model.get_row_data(row)
    
    if card_data:
      self._populate_form(card_data)
      self.current_card_id = card_data.get('id')
  
  def _populate_form(self, card_data: Dict[str, Any]) -> None:
    """
    폼에 카드 정보 채우기
    
    Args:
      card_data: 카드 정보 딕셔너리
    """
    # 카드번호
    self.card_number_input.setText(card_data.get('card_number', ''))
    
    # 마스킹 카드번호
    self.masked_card_number_input.setText(card_data.get('masked_card_number', ''))
    
    # 카드명
    self.card_name_input.setText(card_data.get('card_name', ''))
    
    # 카드유형
    self.card_type_input.setText(card_data.get('card_type', ''))
    
    # 카드사 선택 (인덱스 1부터 검색, 인덱스 0은 "선택" 항목)
    card_company_id = card_data.get('card_company_id')
    if card_company_id:
      for i in range(1, self.card_company_combo.count()):
        if self.card_company_combo.itemData(i) == card_company_id:
          self.card_company_combo.setCurrentIndex(i)
          break
      else:
        # 일치하는 카드사를 찾지 못한 경우 "선택"으로 설정
        self.card_company_combo.setCurrentIndex(0)
    else:
      # 카드사 ID가 없는 경우 "선택"으로 설정
      self.card_company_combo.setCurrentIndex(0)
    
    # 사용여부
    is_active = card_data.get('is_active', True)
    self.is_active_checkbox.setChecked(bool(is_active))
  
  def _get_form_data(self) -> Dict[str, Any]:
    """
    폼에서 데이터 가져오기
    
    Returns:
      폼 데이터 딕셔너리
    """
    # 카드사 ID 가져오기 (인덱스 0이면 "선택" 항목이므로 None 반환)
    card_company_id = None
    current_index = self.card_company_combo.currentIndex()
    if current_index > 0:  # "선택"이 아닌 경우
      card_company_id = self.card_company_combo.currentData()
    
    return {
      'card_number': self.card_number_input.text().strip(),
      'masked_card_number': self.masked_card_number_input.text().strip(),
      'card_name': self.card_name_input.text().strip(),
      'card_type': self.card_type_input.text().strip(),
      'card_company_id': card_company_id,
      'is_active': self.is_active_checkbox.isChecked()
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
      'card_number': '카드번호',
      'masked_card_number': '마스킹 카드번호',
      'card_name': '카드명',
      'card_company_id': '카드사'
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
    
    return True
  
  def _clear_form(self) -> None:
    """
    폼 초기화
    """
    self.card_number_input.clear()
    self.masked_card_number_input.clear()
    self.card_name_input.clear()
    self.card_type_input.clear()
    self.card_company_combo.setCurrentIndex(0)  # "선택" 항목으로 설정
    self.is_active_checkbox.setChecked(True)

