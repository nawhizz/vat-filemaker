## 🚀 바이브 코딩을 위한 단계별 태스크

이 가이드는 핵심 기능부터 차근차근 구현하며 프로그램을 완성해 나가는 데 중점을 둡니다. 각 단계는 이전 단계의 결과물에 의존하며, 점진적인 개발을 목표로 합니다.

### 🌟 Phase 0: 개발 환경 세팅 & 프로젝트 뼈대 잡기

**목표:** 개발 환경을 구축하고 프로젝트의 기본적인 구조와 실행 가능한 최소한의 GUI 윈도우를 만듭니다.

*   **0.1 프로젝트 초기화:**
    *   프로젝트 루트 디렉토리 생성 (예: `vat_helper/`).
    *   `uv`를 사용하여 가상 환경 생성 및 초기화.
    *   `uv init` 및 `uv add pyside6 sqlalchemy pandas openpyxl requests pytest pyside6-fluent-widgets` 명령어로 필수 패키지 설치.
    *   `requirements.txt` 파일 자동 생성 확인.
*   **0.2 기본적인 프로젝트 구조 생성:**
    *   TRD의 `Code Organization & Convention` 섹션을 참조하여 기본적인 폴더 구조 (`app/`, `app/views/`, `app/repositories/` 등) 생성.
*   **0.3 로깅 및 설정 초기화:**
    *   `app/config/settings.py` 및 `app/config/config.ini` 파일 생성 (기본 로깅 설정, DB 경로 등).
    *   `app/utils/logger.py`를 구현하여 `logging` 모듈 설정.
*   **0.4 PySide6 기본 윈도우 띄우기:**
    *   `main.py` 파일 생성 및 `QApplication`, `QMainWindow`를 사용하여 "부가세 도우미"라는 제목의 빈 윈도우를 띄우는 코드 작성.
    *   `PySide6-Fluent-Widgets`를 적용하여 윈도우 스타일을 설정.
    *   실행(`python main.py`)하여 빈 윈도우가 정상적으로 뜨는지 확인.

---

### 🌟 Phase 1: 데이터베이스 기초 다지기 (SQLite + SQLAlchemy)

**목표:** 프로그램의 모든 데이터가 저장될 SQLite 데이터베이스 스키마를 정의하고, SQLAlchemy ORM을 이용해 기본적인 데이터베이스 연동 환경을 구축합니다.

*   **1.1 데이터베이스 스키마 정의 (`schema.py`):**
    *   `app/repositories/schema.py` 파일에 `CardTransaction` 및 `Taxpayer` 모델 클래스 정의. PRD의 요구사항을 반영하여 필드 (예: 카드사, 거래일, 금액, 사업자등록번호 등) 포함.
    *   SQLAlchemy의 `declarative_base`와 `Column`, `Integer`, `String`, `DateTime` 등을 사용하여 ORM 모델 정의.
*   **1.2 데이터베이스 연결 및 세션 관리 (`database.py`):**
    *   `app/repositories/database.py` 파일에 SQLAlchemy 엔진 생성, 테이블 생성, 세션 관리 함수 구현 (예: `init_db()`, `get_session()`).
    *   `main.py`에서 `init_db()`를 호출하여 프로그램 시작 시 데이터베이스가 초기화되도록 연결.
*   **1.3 Repository 패턴 구현 (`card_repository.py`, `taxpayer_repository.py`):**
    *   `app/repositories/card_repository.py`에 `CardRepository` 클래스 생성.
    *   카드 내역 추가 (`add_card_transaction`), 조회 (`get_all_card_transactions`) 등 기본적인 CRUD 메서드 스텁(stub) 구현.
    *   `app/repositories/taxpayer_repository.py`에 `TaxpayerRepository` 클래스 생성.
    *   사업자 정보 추가 (`add_taxpayer`), 조회 (`get_taxpayer_by_reg_no`) 등 기본적인 CRUD 메서드 스텁 구현.
*   **1.4 데이터베이스 초기 동작 테스트:**
    *   콘솔에서 간단한 스크립트를 작성하여 `schema.py`로 정의된 테이블이 `database.py`를 통해 SQLite 파일 내에 생성되는지 확인.
    *   `card_repository`를 통해 더미 데이터를 추가하고 조회해보며 ORM 동작 확인.

---

### 🌟 Phase 2: 엑셀 파일 업로드 및 카드 내역 기본 조회

**목표:** 엑셀 파일을 읽어와 데이터베이스에 저장하고, 저장된 카드 내역을 GUI에서 테이블 형태로 조회하는 기능을 구현합니다.

*   **2.1 엑셀 어댑터 개발 (`excel_adapter.py`):**
    *   `app/adapters/excel_adapter.py`에 `ExcelAdapter` 클래스 생성.
    *   `pandas`와 `openpyxl`을 활용하여 `.xls`, `.xlsx` 파일에서 카드 내역 데이터를 읽는 `read_excel_data(filepath)` 메서드 구현.
    *   읽어온 데이터를 표준화된 `TypedDict` 또는 DTO 형식으로 변환하여 반환하도록 설계.
*   **2.2 카드 서비스 로직 구현 (`card_service.py`):**
    *   `app/services/card_service.py`에 `CardService` 클래스 생성.
    *   `ExcelAdapter`를 사용하여 엑셀 데이터를 읽고, 유효성 검사 (예: 필수 필드 누락 여부) 후 `CardRepository`를 통해 데이터베이스에 저장하는 `upload_excel_to_db(filepath)` 메서드 구현.
    *   데이터베이스에서 카드 내역을 조회하는 `get_card_transactions()` 메서드 구현.
*   **2.3 카드 내역 모델 (`card_transaction_model.py`):**
    *   `app/models/card_transaction_model.py`에 `QAbstractTableModel`을 상속받는 `CardTransactionModel` 구현.
    *   서비스 계층에서 받아온 카드 내역 데이터를 GUI 테이블에 표시할 수 있도록 `data()`, `rowCount()`, `columnCount()`, `headerData()` 메서드 구현.
*   **2.4 카드 내역 조회/편집 UI (`card_view.py`):**
    *   `app/views/card_view.py`에 `CardView` 위젯 생성.
    *   파일 업로드 버튼 (`QPushButton`), 파일 경로 표시 (`QLineEdit`), `QTableView` 위젯 배치.
    *   업로드 버튼 클릭 시 파일 다이얼로그를 열어 엑셀 파일을 선택하고, `CardService`를 통해 데이터를 DB에 저장.
    *   `QTableView`에 `CardTransactionModel`을 연결하여 저장된 카드 내역을 표시.
    *   테이블 새로고침 버튼 및 기본 검색바(`app/views/components/search_bar.py` 스텁 생성) 연동.
*   **2.5 메인 윈도우에 통합:**
    *   `main_window.py`에 `CardView`를 추가하고 메뉴 또는 탭바를 통해 접근할 수 있도록 구성.
    *   프로그램 실행 후 엑셀 파일을 업로드하고 데이터가 테이블에 정상적으로 표시되는지 확인.

---

### 🌟 Phase 3: 사업자 정보 관리 & 국세청 API 연동

**목표:** 사용자의 개인사업자 정보를 등록하고, 국세청 API를 통해 사업자 상태를 조회하며, 그 이력을 관리하는 기능을 구현합니다.

*   **3.1 사업자 정보 스키마 확장 (`schema.py`):**
    *   `app/repositories/schema.py`의 `Taxpayer` 모델에 사업자등록번호, 상호, 대표자명, 주소 등 추가 필드 정의.
    *   사업자 상태(계속/폐업, 과세유형) 및 상태 변경 이력을 위한 별도 테이블 또는 필드 추가.
*   **3.2 국세청 API 연동 (`nts_api.py`):**
    *   `app/api/nts_api.py`에 `NtsApi` 클래스 생성.
    *   `requests` 라이브러리를 사용하여 국세청 '사업자등록상태조회' API를 호출하는 `get_taxpayer_status(reg_no)` 메서드 구현.
    *   API 응답을 파싱하여 필요한 사업자 상태 정보 (예: 사업자등록상태, 과세유형)를 반환. (실제 API는 인증 키가 필요하므로, 개발 단계에서는 더미 응답을 가정하거나 테스트용 키 발급 필요).
*   **3.3 사업자 서비스 로직 구현 (`taxpayer_service.py`):**
    *   `app/services/taxpayer_service.py`에 `TaxpayerService` 클래스 생성.
    *   `TaxpayerRepository`를 통해 사업자 정보 CRUD 구현.
    *   `NtsApi`를 호출하여 사업자 상태를 조회하고, 그 결과를 `Taxpayer` 모델에 업데이트하며 상태 변경 이력을 기록하는 `update_taxpayer_status(reg_no)` 메서드 구현.
*   **3.4 사업자 정보 모델 (`taxpayer_status_model.py`):**
    *   `app/models/taxpayer_status_model.py`에 `QAbstractTableModel`을 상속받는 `TaxpayerStatusModel` 구현 (사업자 목록 및 상태 표시용).
*   **3.5 사업자 상태 관리 UI (`taxpayer_view.py`):**
    *   `app/views/taxpayer_view.py`에 `TaxpayerView` 위젯 생성.
    *   사업자 정보 입력 필드 (등록번호, 상호 등), 저장/수정 버튼, '상태 조회' 버튼 배치.
    *   `QTableView`를 사용하여 등록된 사업자 목록과 각 사업자의 현재 상태 및 이력을 표시.
    *   '상태 조회' 버튼 클릭 시 `TaxpayerService`를 호출하여 국세청 API 연동 및 상태 업데이트.
*   **3.6 메인 윈도우에 통합:**
    *   `main_window.py`에 `TaxpayerView`를 추가하고 접근할 수 있도록 메뉴/탭 추가.

---

### 🌟 Phase 4: 부가세 제외 대상 관리 & 전자 매체 파일 생성

**목표:** 사업자 상태 및 특정 조건에 따라 부가세 신고 대상에서 제외되는 거래를 관리하고, 최종적으로 국세청 양식에 맞는 전자 매체 파일을 생성합니다.

*   **4.1 부가세 서비스 로직 구현 (`vat_service.py`):**
    *   `app/services/vat_service.py`에 `VatService` 클래스 생성.
    *   `TaxpayerService`와 `CardService`를 활용하여 카드 내역 중 부가세 제외 대상을 식별하는 `identify_exclusion_targets()` 메서드 구현:
        *   폐업 사업자와의 거래 자동 제외.
        *   간이과세자/면세 사업자와의 거래 자동 제외.
        *   병원, 약국, 학원 등 특정 업종 수동/자동 제외 처리 로직 구현.
    *   제외 사유를 저장하고 관리하는 기능 추가.
    *   국세청 부가세 신고 양식에 맞는 전자 매체 파일 (텍스트 또는 CSV)을 생성하는 `generate_electronic_file(output_path)` 메서드 구현.
*   **4.2 부가세 제외 모델 (`vat_exclusion_model.py`):**
    *   `app/models/vat_exclusion_model.py`에 `QAbstractTableModel`을 상속받는 모델 구현.
    *   제외 대상 카드 내역과 그 사유를 표시할 수 있도록 구성.
*   **4.3 부가세 제외 대상 관리 UI (`vat_view.py`):**
    *   `app/views/vat_view.py`에 `VatView` 위젯 생성.
    *   카드 내역 중 제외 대상으로 분류된 항목들을 `QTableView`로 표시.
    *   수동으로 제외 대상을 추가/해제하고 제외 사유를 입력할 수 있는 기능 추가.
    *   필터링 및 검색 기능을 통해 제외 대상 내역을 쉽게 관리할 수 있도록 구성.
*   **4.4 전자 매체 파일 생성 UI (`vat_file_creation_view.py`):**
    *   `app/views/vat_file_creation_view.py`에 `VatFileCreationView` 위젯 생성.
    *   파일 저장 경로 설정 (`QLineEdit` 및 `QPushButton`을 이용한 파일 다이얼로그).
    *   '파일 생성' 버튼을 배치하고, 클릭 시 `VatService.generate_electronic_file()` 호출.
    *   생성될 파일의 미리보기 기능 (선택 사항) 또는 생성 완료 메시지 표시.
*   **4.5 메인 윈도우에 통합:**
    *   `main_window.py`에 `VatView`와 `VatFileCreationView`를 추가.

---

### 🌟 Phase 5: 통계, 보고서 & 프로그램 완성도 높이기

**목표:** 월별/분기별 카드 사용 내역 통계 및 보고서 기능을 추가하고, 전반적인 프로그램의 안정성, 사용성, 성능을 개선하며 배포 준비를 합니다.

*   **5.1 통계/보고서 서비스 로직 구현 (`report_service.py`):**
    *   `app/services/report_service.py`에 `ReportService` 클래스 생성.
    *   월별/분기별 카드 사용 내역 집계, 부가세 신고 관련 주요 통계 (예: 과세/면세 거래 비율)를 계산하는 메서드 구현.
    *   `pandas`를 활용하여 데이터 처리 효율화.
*   **5.2 통계/보고서 모델 (`report_model.py`):**
    *   `app/models/report_model.py`에 `QAbstractTableModel` 또는 커스텀 모델 구현 (읽기 전용 집계 데이터 표시용).
*   **5.3 통계/보고서 UI (`report_view.py`):**
    *   `app/views/report_view.py`에 `ReportView` 위젯 생성.
    *   기간 선택 (월별/분기별 드롭다운), 통계 결과 표시를 위한 `QTableView` 또는 간단한 데이터 시각화 라이브러리 (예: `matplotlib`이나 `plotly`의 `PySide6` 통합, 선택 사항) 연동.
    *   보고서 생성 (예: CSV 또는 PDF) 버튼 (선택 사항).
*   **5.4 UI/UX 개선:**
    *   `PySide6-Fluent-Widgets`를 적극 활용하여 모든 화면의 디자인 컨셉 (`심플하고 직관적인 디자인`, `사용자 친화적인 인터페이스`, `세련된 색상 및 레이아웃`)을 최종적으로 적용.
    *   각종 입력 필드 유효성 검사 및 사용자 피드백 (성공/실패 메시지, 진행률 표시).
    *   테이블 필터링/검색 기능 (`QSortFilterProxyModel` 사용) 및 정렬 기능 구현.
    *   날짜 및 금액 표시를 위한 `app/delegates/` 폴더에 `QStyledItemDelegate` 파생 클래스 구현 (예: `money_delegate.py`, `date_delegate.py`).
*   **5.5 성능 최적화:**
    *   대용량 데이터 처리 시 `CardRepository` 및 `CardService`의 데이터베이스 쿼리 최적화 (인덱스 활용).
    *   시간이 오래 걸리는 작업 (엑셀 로딩, API 호출)에 대한 비동기 처리 또는 멀티스레딩 적용 (예: `QThreadPool`, `QRunnable` 또는 `QThread` 활용)하여 UI 멈춤 방지.
*   **5.6 단위 테스트 및 통합 테스트:**
    *   `pytest`를 사용하여 `services`, `repositories`, `adapters` 등 핵심 로직에 대한 단위 테스트 코드 작성 및 실행.
    *   `tests/` 폴더 구조를 TRD에 맞춰 정리.
*   **5.7 배포 준비:**
    *   `PyInstaller` 또는 `cx_Freeze`를 사용하여 Python 코드를 실행 가능한 단일 파일 또는 패키지 형태로 배포하는 스크립트 작성 및 테스트.
    *   `resources/` 폴더에 아이콘, 스타일시트(`qss`) 등 리소스 관리.
    *   최종 `README.md` 작성.

