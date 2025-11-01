"""
카드사 정보 등록 인터페이스

카드사 정보를 등록하고 관리하는 페이지를 구현합니다.
"""

from typing import Optional, Dict, Any, List
from PySide6.QtCore import Qt, Signal, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
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
  TableView
)
from app.services.card_company_service import CardCompanyService
from app.models.card_company_model import CardCompanyModel


class CardCompanyInterface(QWidget):
  """
  카드사 정보 등록 인터페이스
  
  카드사 정보를 등록하고 관리하는 페이지입니다.
  """
  
  # 데이터 변경 시그널
  data_changed = Signal()
  
  def __init__(self):
    super().__init__()
    self.card_company_service = CardCompanyService()
    self.current_card_company_id: Optional[int] = None
    self._init_ui()
    self._connect_signals()
  
  def _init_ui(self) -> None:
    """
    카드사 정보 등록 인터페이스 UI 초기화
    """
    layout = QVBoxLayout(self)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)
    
    # 제목
    title_label = TitleLabel("카드사 정보 관리")
    layout.addWidget(title_label)
    
    # 설명
    description_label = BodyLabel("카드사 정보를 등록하고 관리할 수 있습니다.")
    layout.addWidget(description_label)
    
    # 검색조건 섹션
    search_card = CardWidget()
    search_card.setFixedHeight(80)
    search_layout = QFormLayout(search_card)
    search_layout.setSpacing(15)
    search_layout.setContentsMargins(20, 20, 20, 20)
    
    # 검색조건: 카드사 코드/명칭
    self.search_keyword_input: LineEdit = LineEdit()
    self.search_keyword_input.setPlaceholderText("카드사 코드 또는 명칭으로 검색")
    search_layout.addRow("카드사 검색어", self.search_keyword_input)
    
    layout.addWidget(search_card)
    
    # 카드사 정보 등록 섹션과 버튼 영역을 담을 수평 레이아웃
    main_content_layout = QHBoxLayout()
    main_content_layout.setSpacing(20)
    
    # 카드사 정보 등록 폼 카드
    form_card = CardWidget()
    form_card.setFixedWidth(400)
    form_layout = QFormLayout(form_card)
    form_layout.setSpacing(15)
    form_layout.setContentsMargins(20, 20, 20, 20)
    
    # 카드사 코드
    self.card_company_code_input: LineEdit = LineEdit()
    self.card_company_code_input.setPlaceholderText("카드사 코드를 입력하세요")
    self.card_company_code_input.setMaxLength(3)
    form_layout.addRow("카드사 코드 *", self.card_company_code_input)
    
    # 카드사 한글명
    self.card_company_name_input: LineEdit = LineEdit()
    self.card_company_name_input.setPlaceholderText("카드사 한글명을 입력하세요")
    self.card_company_name_input.setMaxLength(255)
    form_layout.addRow("카드사 한글명 *", self.card_company_name_input)
    
    # 카드사 영문명
    self.card_company_name_en_input: LineEdit = LineEdit()
    self.card_company_name_en_input.setPlaceholderText("카드사 영문명을 입력하세요")
    self.card_company_name_en_input.setMaxLength(255)
    form_layout.addRow("카드사 영문명", self.card_company_name_en_input)
    
    main_content_layout.addWidget(form_card)
    
    # 버튼 영역
    button_layout = QVBoxLayout()
    button_layout.setSpacing(15)
    
    # 조회 버튼
    self.search_button: PrimaryPushButton = PrimaryPushButton("조회")
    button_layout.addWidget(self.search_button)
    
    # 신규 버튼
    self.new_button: PushButton = PushButton("신규")
    button_layout.addWidget(self.new_button)
    
    # 저장 버튼
    self.save_button: PrimaryPushButton = PrimaryPushButton("저장")
    button_layout.addWidget(self.save_button)
    
    # 초기화 버튼
    self.reset_button: PushButton = PushButton("초기화")
    button_layout.addWidget(self.reset_button)
    
    button_layout.addStretch()
    main_content_layout.addLayout(button_layout)
    main_content_layout.addStretch()
    
    layout.addLayout(main_content_layout)
    
    # 카드사 정보 목록 섹션
    list_card = CardWidget()
    list_layout = QVBoxLayout(list_card)
    list_layout.setContentsMargins(20, 20, 20, 20)
    list_layout.setSpacing(10)
    
    # 목록 제목
    list_title = BodyLabel("카드사 정보 목록")
    list_title.setStyleSheet("font-weight: bold; font-size: 14px;")
    list_layout.addWidget(list_title)
    
    # 테이블 뷰 (QFluentWidgets의 TableView 사용)
    self.card_company_table_view: TableView = TableView()
    self.card_company_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.card_company_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.card_company_table_view.setAlternatingRowColors(True)
    self.card_company_table_view.setSortingEnabled(True)
    
    # 테이블 모델 설정
    self.card_company_model = CardCompanyModel(self)
    self.card_company_table_view.setModel(self.card_company_model)
    
    # 컬럼 너비 자동 조절
    header = self.card_company_table_view.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    list_layout.addWidget(self.card_company_table_view)
    
    # 테이블 선택 시 상세 정보를 폼에 표시
    self.card_company_table_view.selectionModel().selectionChanged.connect(
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
    
    # 검색조건 변경 시 조회
    self.search_keyword_input.textChanged.connect(
      self._on_search_condition_changed
    )
  
  def _on_search_condition_changed(self) -> None:
    """
    검색조건 변경 시 자동 조회 (옵션)
    """
    # 자동 조회를 원하지 않으면 이 부분을 비활성화하거나
    # 타이머를 사용하여 입력 완료 후 조회하도록 할 수 있습니다.
    pass
  
  def _on_search_button_clicked(self) -> None:
    """
    조회 버튼 클릭 이벤트 처리
    """
    try:
      # 검색조건 가져오기
      keyword = self.search_keyword_input.text().strip()
      
      # 검색 파라미터 설정
      search_params = {}
      if keyword:
        # 키워드가 카드사 코드인지 명칭인지 구분
        # 간단하게 명칭으로 검색하도록 설정 (필요시 로직 추가 가능)
        # 3자리 이하면 코드로, 그 이상이면 명칭으로 검색
        if len(keyword) <= 3:
          search_params['card_company_code'] = keyword
        else:
          search_params['card_company_name'] = keyword
      
      # 검색 실행
      results = self.card_company_service.search_card_companies(**search_params)
      
      # 테이블 모델에 데이터 설정
      self.card_company_model.set_data(results)
      
      # 조회 결과 메시지
      InfoBar.success(
        title="조회 완료",
        content=f"총 {len(results)}건의 카드사 정보를 찾았습니다.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      
    except Exception as e:
      InfoBar.error(
        title="조회 오류",
        content=f"카드사 정보 조회 중 오류가 발생했습니다: {str(e)}",
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
    self.current_card_company_id = None
    # 테이블 선택 해제
    self.card_company_table_view.clearSelection()
  
  def _on_save_button_clicked(self) -> None:
    """
    저장 버튼 클릭 이벤트 처리
    """
    data = self._get_form_data()
    
    if not self._validate_form_data(data):
      return
    
    try:
      card_company_data = {
        'card_company_code': data['card_company_code'],
        'card_company_name': data['card_company_name'],
        'card_company_name_en': data.get('card_company_name_en', '') or None
      }
      
      if self.current_card_company_id:
        # 수정 모드
        updated = self.card_company_service.update_card_company(
          self.current_card_company_id,
          card_company_data
        )
        
        if updated:
          InfoBar.success(
            title="수정 완료",
            content="카드사 정보가 성공적으로 수정되었습니다.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
          )
      else:
        # 등록 모드
        created = self.card_company_service.create_card_company(
          card_company_data
        )
        
        if created:
          InfoBar.success(
            title="등록 완료",
            content="카드사 정보가 성공적으로 등록되었습니다.",
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
        content=f"카드사 정보 저장 중 오류가 발생했습니다: {str(e)}",
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
    self.current_card_company_id = None
    self.card_company_table_view.clearSelection()
    self.search_keyword_input.clear()
    self.card_company_model.clear()
  
  def _on_table_selection_changed(self) -> None:
    """
    테이블 선택 변경 이벤트 처리
    """
    selected_indexes = self.card_company_table_view.selectionModel().selectedRows()
    
    if not selected_indexes:
      return
    
    # 첫 번째 선택된 행 가져오기
    row = selected_indexes[0].row()
    card_company_data = self.card_company_model.get_row_data(row)
    
    if card_company_data:
      self._populate_form(card_company_data)
      self.current_card_company_id = card_company_data.get('id')
  
  def _populate_form(self, card_company_data: Dict[str, Any]) -> None:
    """
    폼에 카드사 정보 채우기
    
    Args:
      card_company_data: 카드사 정보 딕셔너리
    """
    # 카드사 코드
    self.card_company_code_input.setText(card_company_data.get('card_company_code', ''))
    
    # 카드사 한글명
    self.card_company_name_input.setText(card_company_data.get('card_company_name', ''))
    
    # 카드사 영문명
    self.card_company_name_en_input.setText(card_company_data.get('card_company_name_en', ''))
  
  def _get_form_data(self) -> Dict[str, Any]:
    """
    폼에서 데이터 가져오기
    
    Returns:
      폼 데이터 딕셔너리
    """
    return {
      'card_company_code': self.card_company_code_input.text().strip(),
      'card_company_name': self.card_company_name_input.text().strip(),
      'card_company_name_en': self.card_company_name_en_input.text().strip()
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
      'card_company_code': '카드사 코드',
      'card_company_name': '카드사 한글명'
    }
    
    for field, field_name in required_fields.items():
      if not data[field]:
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
    self.card_company_code_input.clear()
    self.card_company_name_input.clear()
    self.card_company_name_en_input.clear()

