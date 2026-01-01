"""
카드사용내역 등록 인터페이스

카드사용내역 엑셀 파일을 업로드하고 등록하는 페이지를 구현합니다.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
  QWidget, 
  QVBoxLayout, 
  QHBoxLayout, 
  QFileDialog,
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
  FluentIcon
)
from app.services.card_transaction_service import CardTransactionService
from app.services.card_company_service import CardCompanyService
from app.models.card_transaction_model import CardTransactionModel


class CardTransactionInterface(QWidget):
  """
  카드사용내역 등록 인터페이스
  
  엑셀 파일에서 카드사용내역을 읽어 등록하는 페이지입니다.
  """
  
  # 데이터 변경 시그널
  data_changed = Signal()
  
  def __init__(self):
    super().__init__()
    self.transaction_service = CardTransactionService()
    self.card_company_service = CardCompanyService()
    self.selected_file_path: Optional[str] = None
    self.excel_data: List[Dict[str, Any]] = []
    self._init_ui()
    self._connect_signals()
    self._load_card_companies()
  
  def _init_ui(self) -> None:
    """
    카드사용내역 등록 인터페이스 UI 초기화
    """
    layout = QVBoxLayout(self)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)
    
    # 제목
    title_label = TitleLabel("카드사용내역 등록")
    layout.addWidget(title_label)
    
    # 설명
    description_label = BodyLabel("카드사를 선택하고 엑셀 파일을 업로드하여 카드사용내역을 일괄 등록할 수 있습니다.")
    layout.addWidget(description_label)
    
    # 파일 선택 섹션
    file_card = CardWidget()
    file_card.setFixedHeight(100)
    file_layout = QVBoxLayout(file_card)
    file_layout.setSpacing(15)
    file_layout.setContentsMargins(20, 20, 20, 20)
    
    # 첫 번째 줄: 카드사 선택
    first_row = QHBoxLayout()
    first_row.setSpacing(15)
    
    card_company_label = BodyLabel("카드사:")
    first_row.addWidget(card_company_label)
    
    self.card_company_combo: ComboBox = ComboBox()
    self.card_company_combo.setPlaceholderText("카드사를 선택하세요")
    self.card_company_combo.setFixedWidth(250)
    first_row.addWidget(self.card_company_combo)
    
    first_row.addStretch()
    file_layout.addLayout(first_row)
    
    # 두 번째 줄: 파일 선택
    second_row = QHBoxLayout()
    second_row.setSpacing(15)
    
    file_label = BodyLabel("엑셀 파일:")
    second_row.addWidget(file_label)
    
    self.file_path_input: LineEdit = LineEdit()
    self.file_path_input.setPlaceholderText("엑셀 파일을 선택하세요")
    self.file_path_input.setReadOnly(True)
    second_row.addWidget(self.file_path_input)
    
    self.file_select_button: PushButton = PushButton("파일 선택", icon=FluentIcon.FOLDER)
    second_row.addWidget(self.file_select_button)
    
    self.file_load_button: PrimaryPushButton = PrimaryPushButton("불러오기", icon=FluentIcon.DOWN)
    second_row.addWidget(self.file_load_button)
    
    file_layout.addLayout(second_row)
    layout.addWidget(file_card)
    
    # 버튼 영역
    button_layout = QHBoxLayout()
    button_layout.setSpacing(15)
    
    # 전체 선택 버튼
    self.select_all_button: PushButton = PushButton("전체 선택", icon=FluentIcon.ACCEPT)
    button_layout.addWidget(self.select_all_button)
    
    # 선택 해제 버튼
    self.deselect_all_button: PushButton = PushButton("선택 해제", icon=FluentIcon.CANCEL)
    button_layout.addWidget(self.deselect_all_button)
    
    button_layout.addStretch()
    
    # 초기화 버튼
    self.reset_button: PushButton = PushButton("초기화", icon=FluentIcon.ROTATE)
    button_layout.addWidget(self.reset_button)
    
    # 등록 버튼
    self.register_button: PrimaryPushButton = PrimaryPushButton("등록", icon=FluentIcon.ACCEPT)
    self.register_button.setEnabled(False)
    button_layout.addWidget(self.register_button)
    
    layout.addLayout(button_layout)
    
    # 데이터 목록 섹션
    list_card = CardWidget()
    list_layout = QVBoxLayout(list_card)
    list_layout.setContentsMargins(20, 20, 20, 20)
    list_layout.setSpacing(10)
    
    # 목록 제목
    list_title = BodyLabel("카드사용내역 목록")
    list_title.setStyleSheet("font-weight: bold; font-size: 14px;")
    list_layout.addWidget(list_title)
    
    # 테이블 뷰
    self.transaction_table_view: TableView = TableView()
    self.transaction_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.transaction_table_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
    self.transaction_table_view.setAlternatingRowColors(True)
    self.transaction_table_view.setSortingEnabled(True)
    
    # 테이블 모델 설정
    self.transaction_model = CardTransactionModel(self)
    self.transaction_table_view.setModel(self.transaction_model)
    
    # 컬럼 너비 자동 조절
    header = self.transaction_table_view.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)  # 거래처명 컬럼 늘리기
    
    list_layout.addWidget(self.transaction_table_view)
    
    layout.addWidget(list_card)
  
  def _connect_signals(self) -> None:
    """
    시그널 연결
    """
    # 버튼 클릭 이벤트
    self.file_select_button.clicked.connect(self._on_file_select_button_clicked)
    self.file_load_button.clicked.connect(self._on_file_load_button_clicked)
    self.select_all_button.clicked.connect(self._on_select_all_button_clicked)
    self.deselect_all_button.clicked.connect(self._on_deselect_all_button_clicked)
    self.reset_button.clicked.connect(self._on_reset_button_clicked)
    self.register_button.clicked.connect(self._on_register_button_clicked)
  
  def _load_card_companies(self) -> None:
    """
    카드사 목록 로드
    """
    try:
      card_companies = self.card_company_service.get_all_card_companies()
      
      # 콤보박스 초기화 및 "선택" 항목 추가
      self.card_company_combo.clear()
      self.card_company_combo.addItem("선택하세요", userData=None)
      
      for company in card_companies:
        company_name = company.get('card_company_name', '')
        company_id = company.get('id')
        self.card_company_combo.addItem(company_name, userData=company_id)
      
    except Exception as e:
      InfoBar.warning(
        title="경고",
        content=f"카드사 목록을 불러오는 중 오류가 발생했습니다: {str(e)}",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=self
      )
  
  def _on_file_select_button_clicked(self) -> None:
    """
    파일 선택 버튼 클릭 이벤트 처리
    """
    file_path, _ = QFileDialog.getOpenFileName(
      self,
      "엑셀 파일 선택",
      "",
      "Excel Files (*.xlsx *.xls);;All Files (*)"
    )
    
    if file_path:
      self.selected_file_path = file_path
      self.file_path_input.setText(file_path)
      InfoBar.success(
        title="파일 선택",
        content=f"파일이 선택되었습니다: {Path(file_path).name}",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
  
  def _on_file_load_button_clicked(self) -> None:
    """
    불러오기 버튼 클릭 이벤트 처리
    """
    # 카드사 선택 확인
    card_company_id = self.card_company_combo.currentData()
    if not card_company_id:
      InfoBar.warning(
        title="입력 오류",
        content="카드사를 먼저 선택하세요.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      return
    
    # 파일 선택 확인
    if not self.selected_file_path:
      InfoBar.warning(
        title="입력 오류",
        content="엑셀 파일을 먼저 선택하세요.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      return
    
    try:
      # 엑셀 파일 읽기
      from app.utils.excel_reader import read_card_transaction_excel
      
      self.excel_data = read_card_transaction_excel(
        self.selected_file_path, 
        card_company_id
      )
      
      if not self.excel_data:
        InfoBar.warning(
          title="알림",
          content="엑셀 파일에 데이터가 없습니다.",
          orient=Qt.Horizontal,
          isClosable=True,
          position=InfoBarPosition.TOP,
          duration=1000,
          parent=self
        )
        return
      
      # 테이블에 데이터 표시
      self.transaction_model.set_data(self.excel_data)
      
      # 등록 버튼 활성화
      self.register_button.setEnabled(True)
      
      InfoBar.success(
        title="불러오기 완료",
        content=f"총 {len(self.excel_data)}건의 데이터를 불러왔습니다.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      
    except Exception as e:
      InfoBar.error(
        title="파일 읽기 오류",
        content=f"엑셀 파일을 읽는 중 오류가 발생했습니다: {str(e)}",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=self
      )
  
  def _on_select_all_button_clicked(self) -> None:
    """
    전체 선택 버튼 클릭 이벤트 처리
    """
    self.transaction_table_view.selectAll()
  
  def _on_deselect_all_button_clicked(self) -> None:
    """
    선택 해제 버튼 클릭 이벤트 처리
    """
    self.transaction_table_view.clearSelection()
  
  def _on_reset_button_clicked(self) -> None:
    """
    초기화 버튼 클릭 이벤트 처리
    """
    self.card_company_combo.setCurrentIndex(0)
    self.file_path_input.clear()
    self.selected_file_path = None
    self.excel_data = []
    self.transaction_model.clear()
    self.register_button.setEnabled(False)
    
    InfoBar.info(
      title="초기화",
      content="모든 입력이 초기화되었습니다.",
      orient=Qt.Horizontal,
      isClosable=True,
      position=InfoBarPosition.TOP,
      duration=1000,
      parent=self
    )
  
  def _on_register_button_clicked(self) -> None:
    """
    등록 버튼 클릭 이벤트 처리
    """
    if not self.excel_data:
      InfoBar.warning(
        title="등록 오류",
        content="등록할 데이터가 없습니다.",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=1000,
        parent=self
      )
      return
    
    try:
      # 선택된 행만 등록
      selected_indexes = self.transaction_table_view.selectionModel().selectedRows()
      
      if not selected_indexes:
        InfoBar.warning(
          title="등록 오류",
          content="등록할 행을 선택하세요.",
          orient=Qt.Horizontal,
          isClosable=True,
          position=InfoBarPosition.TOP,
          duration=1000,
          parent=self
        )
        return
      
      # 선택된 행의 데이터만 추출
      selected_data = []
      for index in selected_indexes:
        row = index.row()
        row_data = self.transaction_model.get_row_data(row)
        if row_data:
          selected_data.append(row_data)
      
      # 데이터베이스에 등록
      success_count = 0
      fail_count = 0
      
      for data in selected_data:
        try:
          self.transaction_service.create_transaction(data)
          success_count += 1
        except Exception as e:
          fail_count += 1
          print(f"등록 실패: {str(e)}")
      
      # 결과 메시지
      if success_count > 0:
        InfoBar.success(
          title="등록 완료",
          content=f"총 {success_count}건이 등록되었습니다. (실패: {fail_count}건)",
          orient=Qt.Horizontal,
          isClosable=True,
          position=InfoBarPosition.TOP,
          duration=2000,
          parent=self
        )
        
        # 등록 후 초기화
        self._on_reset_button_clicked()
        
        # 데이터 변경 시그널 발생
        self.data_changed.emit()
      else:
        InfoBar.error(
          title="등록 실패",
          content=f"데이터 등록에 실패했습니다. (실패: {fail_count}건)",
          orient=Qt.Horizontal,
          isClosable=True,
          position=InfoBarPosition.TOP,
          duration=2000,
          parent=self
        )
      
    except Exception as e:
      InfoBar.error(
        title="등록 오류",
        content=f"데이터 등록 중 오류가 발생했습니다: {str(e)}",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=self
      )
