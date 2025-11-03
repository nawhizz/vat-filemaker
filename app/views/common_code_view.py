"""
공통코드 등록 인터페이스

공통코드를 등록하고 관리하는 페이지를 구현합니다.
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
  TableView,
  CheckBox,
  SpinBox
)
from app.services.common_code_service import CommonCodeService
from app.models.common_code_model import CommonCodeModel


class CommonCodeInterface(QWidget):
  """
  공통코드 등록 인터페이스
  
  공통코드를 등록하고 관리하는 페이지입니다.
  """
  
  # 데이터 변경 시그널
  data_changed = Signal()
  
  def __init__(self):
    super().__init__()
    self.common_code_service = CommonCodeService()
    self.current_code_group: Optional[str] = None
    self.current_code: Optional[str] = None
    self._init_ui()
    self._connect_signals()
  
  def _init_ui(self) -> None:
    """
    공통코드 등록 인터페이스 UI 초기화
    """
    layout = QVBoxLayout(self)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)
    
    # 제목
    title_label = TitleLabel("공통코드 관리")
    layout.addWidget(title_label)
    
    # 설명
    description_label = BodyLabel("공통코드를 등록하고 관리할 수 있습니다.")
    layout.addWidget(description_label)
    
    # 검색조건 섹션
    search_card = CardWidget()
    search_card.setFixedHeight(100)
    search_layout = QFormLayout(search_card)
    search_layout.setSpacing(15)
    search_layout.setContentsMargins(20, 20, 20, 20)
    
    # 검색조건: 코드 그룹
    self.search_code_group_input: LineEdit = LineEdit()
    self.search_code_group_input.setPlaceholderText("코드 그룹으로 검색")
    search_layout.addRow("코드 그룹", self.search_code_group_input)
    
    # 검색조건: 코드 또는 코드명
    self.search_keyword_input: LineEdit = LineEdit()
    self.search_keyword_input.setPlaceholderText("코드, 코드명, 코드약어명으로 검색")
    search_layout.addRow("검색어", self.search_keyword_input)
    
    layout.addWidget(search_card)
    
    # 공통코드 등록 섹션과 버튼 영역을 담을 수평 레이아웃
    main_content_layout = QHBoxLayout()
    main_content_layout.setSpacing(20)
    
    # 공통코드 등록 폼 카드
    form_card = CardWidget()
    form_card.setFixedWidth(450)
    form_layout = QFormLayout(form_card)
    form_layout.setSpacing(15)
    form_layout.setContentsMargins(20, 20, 20, 20)
    
    # 코드 그룹
    self.code_group_input: LineEdit = LineEdit()
    self.code_group_input.setPlaceholderText("코드 그룹명을 입력하세요")
    self.code_group_input.setMaxLength(100)
    form_layout.addRow("코드 그룹 *", self.code_group_input)
    
    # 코드
    self.code_input: LineEdit = LineEdit()
    self.code_input.setPlaceholderText("코드 값을 입력하세요")
    self.code_input.setMaxLength(100)
    form_layout.addRow("코드 *", self.code_input)
    
    # 코드명
    self.code_name_input: LineEdit = LineEdit()
    self.code_name_input.setPlaceholderText("코드명을 입력하세요")
    self.code_name_input.setMaxLength(255)
    form_layout.addRow("코드명 *", self.code_name_input)
    
    # 코드약어명
    self.code_abbr_input: LineEdit = LineEdit()
    self.code_abbr_input.setPlaceholderText("코드약어명을 입력하세요")
    self.code_abbr_input.setMaxLength(255)
    form_layout.addRow("코드약어명 *", self.code_abbr_input)
    
    # 정렬 순서
    self.sort_order_input: SpinBox = SpinBox()
    self.sort_order_input.setMinimum(0)
    self.sort_order_input.setMaximum(9999)
    self.sort_order_input.setValue(0)
    form_layout.addRow("정렬 순서", self.sort_order_input)
    
    # 사용여부
    self.is_active_checkbox: CheckBox = CheckBox("사용")
    self.is_active_checkbox.setChecked(True)
    form_layout.addRow("사용여부", self.is_active_checkbox)
    
    # 비고
    self.description_input: LineEdit = LineEdit()
    self.description_input.setPlaceholderText("비고를 입력하세요")
    form_layout.addRow("비고", self.description_input)
    
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
    
    # 삭제 버튼
    self.delete_button: PushButton = PushButton("삭제")
    button_layout.addWidget(self.delete_button)
    
    # 초기화 버튼
    self.reset_button: PushButton = PushButton("초기화")
    button_layout.addWidget(self.reset_button)
    
    button_layout.addStretch()
    main_content_layout.addLayout(button_layout)
    main_content_layout.addStretch()
    
    layout.addLayout(main_content_layout)
    
    # 공통코드 목록 섹션
    list_card = CardWidget()
    list_layout = QVBoxLayout(list_card)
    list_layout.setContentsMargins(20, 20, 20, 20)
    list_layout.setSpacing(10)
    
    # 목록 제목
    list_title = BodyLabel("공통코드 목록")
    list_title.setStyleSheet("font-weight: bold; font-size: 14px;")
    list_layout.addWidget(list_title)
    
    # 테이블 뷰 (QFluentWidgets의 TableView 사용)
    self.common_code_table_view: TableView = TableView()
    self.common_code_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.common_code_table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.common_code_table_view.setAlternatingRowColors(True)
    self.common_code_table_view.setSortingEnabled(True)
    
    # 테이블 모델 설정
    self.common_code_model = CommonCodeModel(self)
    self.common_code_table_view.setModel(self.common_code_model)
    
    # 컬럼 너비 자동 조절
    header = self.common_code_table_view.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    list_layout.addWidget(self.common_code_table_view)
    
    # 테이블 선택 시 상세 정보를 폼에 표시
    self.common_code_table_view.selectionModel().selectionChanged.connect(
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
    self.delete_button.clicked.connect(self._on_delete_button_clicked)
    self.reset_button.clicked.connect(self._on_reset_button_clicked)
  
  def _on_search_button_clicked(self) -> None:
    """
    조회 버튼 클릭 이벤트 처리
    """
    try:
      # 검색조건 가져오기
      code_group = self.search_code_group_input.text().strip()
      keyword = self.search_keyword_input.text().strip()
      
      # 검색 파라미터 설정
      search_params = {}
      if code_group:
        search_params['code_group'] = code_group
      
      if keyword:
        # 키워드는 code, code_name, code_abbr 중 하나로 검색
        # 간단하게 code_name으로 검색 (필요시 로직 추가 가능)
        search_params['code_name'] = keyword
      
      # 검색 실행
      results = self.common_code_service.search_common_codes(**search_params)
      
      # 테이블 모델에 데이터 설정
      self.common_code_model.set_data(results)
      
      # 조회 결과 메시지
      InfoBar.success(
        title="조회 완료",
        content=f"총 {len(results)}건의 공통코드를 찾았습니다.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      
    except Exception as e:
      InfoBar.error(
        title="조회 오류",
        content=f"공통코드 조회 중 오류가 발생했습니다: {str(e)}",
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
    self.current_code_group = None
    self.current_code = None
    # 테이블 선택 해제
    self.common_code_table_view.clearSelection()
  
  def _on_save_button_clicked(self) -> None:
    """
    저장 버튼 클릭 이벤트 처리
    """
    data = self._get_form_data()
    
    if not self._validate_form_data(data):
      return
    
    try:
      common_code_data = {
        'code_group': data['code_group'],
        'code': data['code'],
        'code_name': data['code_name'],
        'code_abbr': data['code_abbr'],
        'sort_order': data.get('sort_order', 0),
        'is_active': data.get('is_active', True),
        'description': data.get('description', '') or None
      }
      
      if self.current_code_group and self.current_code:
        # 수정 모드
        updated = self.common_code_service.update_common_code(
          self.current_code_group,
          self.current_code,
          common_code_data
        )
        
        if updated:
          InfoBar.success(
            title="수정 완료",
            content="공통코드가 성공적으로 수정되었습니다.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
          )
          # 현재 키 값 업데이트 (수정 시 코드 그룹과 코드가 변경될 수 없으므로 동일)
          self.current_code_group = updated.get('code_group')
          self.current_code = updated.get('code')
      else:
        # 등록 모드
        created = self.common_code_service.create_common_code(
          common_code_data
        )
        
        if created:
          InfoBar.success(
            title="등록 완료",
            content="공통코드가 성공적으로 등록되었습니다.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
          )
          # 등록 후 현재 키 값 설정
          self.current_code_group = common_code_data['code_group']
          self.current_code = common_code_data['code']
      
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
        content=f"공통코드 저장 중 오류가 발생했습니다: {str(e)}",
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
    if not self.current_code_group or not self.current_code:
      InfoBar.warning(
        title="삭제 오류",
        content="삭제할 공통코드를 선택해주세요.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      return
    
    try:
      deleted = self.common_code_service.delete_common_code(
        self.current_code_group,
        self.current_code
      )
      
      if deleted:
        InfoBar.success(
          title="삭제 완료",
          content="공통코드가 성공적으로 삭제되었습니다.",
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
          content="공통코드 삭제에 실패했습니다.",
          orient=Qt.Horizontal,
          isClosable=True,
          position=InfoBarPosition.TOP,
          duration=1000,
          parent=self
        )
        
    except Exception as e:
      InfoBar.error(
        title="삭제 오류",
        content=f"공통코드 삭제 중 오류가 발생했습니다: {str(e)}",
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
    self.current_code_group = None
    self.current_code = None
    self.common_code_table_view.clearSelection()
    self.search_code_group_input.clear()
    self.search_keyword_input.clear()
    self.common_code_model.clear()
  
  def _on_table_selection_changed(self) -> None:
    """
    테이블 선택 변경 이벤트 처리
    """
    selected_indexes = self.common_code_table_view.selectionModel().selectedRows()
    
    if not selected_indexes:
      return
    
    # 첫 번째 선택된 행 가져오기
    row = selected_indexes[0].row()
    common_code_data = self.common_code_model.get_row_data(row)
    
    if common_code_data:
      self._populate_form(common_code_data)
      self.current_code_group = common_code_data.get('code_group')
      self.current_code = common_code_data.get('code')
  
  def _populate_form(self, common_code_data: Dict[str, Any]) -> None:
    """
    폼에 공통코드 정보 채우기
    
    Args:
      common_code_data: 공통코드 정보 딕셔너리
    """
    # 코드 그룹
    self.code_group_input.setText(common_code_data.get('code_group', ''))
    
    # 코드
    self.code_input.setText(common_code_data.get('code', ''))
    
    # 코드명
    self.code_name_input.setText(common_code_data.get('code_name', ''))
    
    # 코드약어명
    self.code_abbr_input.setText(common_code_data.get('code_abbr', ''))
    
    # 정렬 순서
    self.sort_order_input.setValue(common_code_data.get('sort_order', 0))
    
    # 사용여부
    is_active = common_code_data.get('is_active', True)
    self.is_active_checkbox.setChecked(bool(is_active))
    
    # 비고
    self.description_input.setText(common_code_data.get('description', ''))
  
  def _get_form_data(self) -> Dict[str, Any]:
    """
    폼에서 데이터 가져오기
    
    Returns:
      폼 데이터 딕셔너리
    """
    return {
      'code_group': self.code_group_input.text().strip(),
      'code': self.code_input.text().strip(),
      'code_name': self.code_name_input.text().strip(),
      'code_abbr': self.code_abbr_input.text().strip(),
      'sort_order': self.sort_order_input.value(),
      'is_active': self.is_active_checkbox.isChecked(),
      'description': self.description_input.text().strip()
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
      'code_group': '코드 그룹',
      'code': '코드',
      'code_name': '코드명',
      'code_abbr': '코드약어명'
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
    self.code_group_input.clear()
    self.code_input.clear()
    self.code_name_input.clear()
    self.code_abbr_input.clear()
    self.sort_order_input.setValue(0)
    self.is_active_checkbox.setChecked(True)
    self.description_input.clear()

