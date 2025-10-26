# Technical Requirements Document (TRD)

## 1. Executive Technical Summary

  - **Project Overview**: 개인 사업자를 위한 부가세 신고 도우미 프로그램을 개발합니다. 엑셀 카드 사용 내역을 SQLite 데이터베이스에 저장하고, 국세청 API를 통해 사업자 상태를 확인하여 부가세 신고 대상/제외 대상을 관리하며, 최종적으로 전자 매체 파일을 생성합니다. Python, PySide6, SQLite를 사용하여 Windows, macOS 데스크톱 애플리케이션으로 개발합니다.
  - **Core Technology Stack**: Python, PySide6, SQLite를 핵심 기술 스택으로 사용합니다. Python은 프로그램 로직 및 데이터 처리에 사용되며, PySide6는 사용자 인터페이스 개발에 사용됩니다. SQLite는 데이터 저장을 위한 경량 데이터베이스로 사용됩니다.
  - **Key Technical Objectives**: 빠르고 안정적인 데이터 처리, 직관적인 사용자 인터페이스, 안전한 데이터 보안을 목표로 합니다. 엑셀 파일 로딩, 데이터베이스 저장, 사업자 상태 조회, 전자 매체 파일 생성 등 주요 기능의 성능을 최적화합니다.
  - **Critical Technical Assumptions**: 국세청 '사업자등록상태조회' API가 안정적으로 제공되며, 엑셀 파일 형식이 일정함을 가정합니다. 또한, 사용자 PC 환경에서 Python, PySide6, SQLite가 정상적으로 설치 및 실행될 수 있음을 가정합니다.

## 2. Tech Stack

| Category | Technology / Library | Reasoning (Why it's chosen for this project) |
| --- | --- | --- |
| 패키지, 개발환경 | uv | 프로젝트 단위 의존성 관리, 패키지 설치 속도, 격리된 환경 제공, 빌드 및 배포 지원까지 통합적으로 제공 |
| 언어 | Python | 높은 생산성, 다양한 라이브러리 지원, 크로스 플랫폼 개발 용이성 |
| GUI 프레임워크 | PySide6 | Qt 기반의 강력한 GUI 기능, Python과의 호환성, 크로스 플랫폼 지원 |
| 데이터베이스 | SQLite | 경량 데이터베이스, 별도 서버 불필요, 간편한 설치 및 관리, SQLAlchemy (ORM) 사용 |
| 엑셀 처리 | pandas, openpyxl | 엑셀 파일 읽기 및 쓰기 기능 제공, 다양한 엑셀 형식 지원 (.xls, .xlsx) |
| API 통신 | requests | 간단하고 효율적인 HTTP 요청 라이브러리 (국세청 API 연동용) |
| 데이터 유효성 검사 | jsonschema | JSON 데이터의 유효성 검사, 데이터 무결성 유지 |
| 로깅 | loguru | 프로그램 실행 중 발생하는 이벤트 기록 및 디버깅, 구조화된 로깅 및 향상된 포맷팅 제공 |
| 단위 테스트 | pytest | 코드의 정확성 및 안정성 검증 |
| UI 디자인 | PySide6-Fluent-Widgets | Fluent Design 스타일 (PRD의 심플하고 직관적인 디자인 컨셉 반영) |
| 배포 | PyInstaller / cx\_Freeze | Python 코드를 실행 가능한 실행 파일로 패키징 |

## 3. System Architecture Design

### Top-Level building blocks

  - **UI (PySide6)**: 사용자 인터페이스를 담당합니다.
      - 메인 화면
      - 카드 내역 조회/편집 화면
      - 사업자 상태 관리 화면
      - 부가세 제외 대상 관리 화면
      - 전자 매체 파일 생성 화면
      - 통계/보고서 화면 (선택 사항)
  - **Business Logic (Python)**: 프로그램의 핵심 로직을 담당합니다.
      - 엑셀 파일 파싱 및 데이터 추출
      - 데이터베이스 연동 및 관리
      - 국세청 API 연동
      - 부가세 계산 및 전자 매체 파일 생성
      - 통계 및 보고서 생성 (선택 사항)
  - **Data Access (Python, SQLite, SQLAlchemy)**: 데이터베이스와의 연동을 담당합니다.
      - SQLite 데이터베이스 연결 관리
      - 데이터 CRUD (Create, Read, Update, Delete)
      - 데이터베이스 스키마 관리 (SQLAlchemy ORM 사용)
  - **API Integration (Python, requests)**: 국세청 '사업자등록상태조회' API와의 연동을 담당합니다.
      - API 요청 및 응답 처리
      - API 데이터 파싱 및 저장
      - API 오류 처리

### Top-Level Component Interaction Diagram

```mermaid
graph TD
    A[UI (PySide6)] --> B[Business Logic (Python)]
    B --> C[Data Access (Python, SQLite, SQLAlchemy)]
    B --> D[API Integration (Python, requests)]
    D --> E[국세청 API]
```

  - UI (PySide6)는 사용자의 입력을 받아 Business Logic (Python)에 전달하고, 결과를 화면에 표시합니다.
  - Business Logic (Python)은 UI로부터 요청을 받아 Data Access (Python, SQLite, SQLAlchemy)를 통해 데이터베이스에 접근하거나, API Integration (Python, requests)을 통해 국세청 API를 호출합니다.
  - Data Access (Python, SQLite, SQLAlchemy)는 Business Logic (Python)의 요청에 따라 데이터베이스에 데이터를 저장, 조회, 수정, 삭제합니다.
  - API Integration (Python, requests)는 Business Logic (Python)의 요청에 따라 국세청 API를 호출하고, 결과를 Business Logic (Python)에 전달합니다.

### Code Organization & Convention

**Domain-Driven Organization Strategy**

  - **Domain Separation**: `card_data`, `taxpayer`, `vat_report`와 같이 비즈니스 도메인별로 코드 분리
  - **Layer-Based Architecture**: `ui`, `logic`, `data`, `api` 레이어로 분리하여 관심사 분리
  - **Feature-Based Modules**: 카드 내역 관리, 사업자 상태 관리, 부가세 신고 관련 기능들을 모듈로 구성
  - **Shared Components**: 공통 유틸리티, 타입, 재사용 가능한 컴포넌트를 `utils` 모듈에 배치
  - **Extensibility**: 이러한 서비스(`services`)와 데이터 접근(`repositories`) 계층의 분리는 PRD 6.에서 요구하는 향후 FastAPI 기반 웹 애플리케이션으로의 전환 용이성을 고려한 설계입니다.

**Universal File & Folder Structure**

```
/
├── main.py
├── app/
│   ├── views/                     # View(위젯) = 화면 & 사용자 상호작용
│   │   ├── main_window.py
│   │   ├── card_view.py           # QListView/QTableView 기반 화면
│   │   ├── taxpayer_view.py       #
│   │   ├── vat_view.py            #
│   │   ├── report_view.py         #
│   │   └── components/            # 공통 위젯(검색바, 페이저 등)
│   │       └── search_bar.py
│   ├── models/                    # QAbstractItemModel 파생
│   │   ├── card_transaction_model.py    # QAbstractTableModel
│   │   ├── taxpayer_status_model.py     # QAbstractTableModel
│   │   ├── vat_exclusion_model.py       # QAbstractTableModel
│   │   └── report_model.py              # 읽기전용 모델(집계)
│   ├── delegates/                 # 셀 렌더링/에디팅
│   │   ├── money_delegate.py
│   │   ├── date_delegate.py
│   │   └── status_badge_delegate.py
│   ├── proxies/                   # 정렬/필터/그룹핑 (QSortFilterProxyModel 등)
│   │   ├── card_filter_proxy.py
│   │   └── taxpayer_filter_proxy.py
│   ├── services/                  # 도메인 로직(계산/규칙/조합)
│   │   ├── card_service.py
│   │   ├── taxpayer_service.py    # 사업자 상태 조회/관리 로직
│   │   ├── vat_service.py         # 제외 대상 처리, 전자 파일 생성 로직
│   │   └── report_service.py
│   ├── repositories/              # 데이터 접근(DAO)
│   │   ├── database.py
│   │   ├── card_repository.py
│   │   ├── taxpayer_repository.py # 사업자 정보 및 상태 변경 이력 관리
│   │   └── schema.py              # ORM/테이블 정의 (SQLAlchemy)
│   ├── api/                       # 외부 API 연동
│   │   └── nts_api.py             # 국세청 API
│   ├── adapters/                  # 입출력 어댑터(엑셀/CSV/포맷)
│   │   └── excel_adapter.py
│   ├── config/
│   │   ├── settings.py            # 설정 객체화(ini 로딩)
│   │   └── config.ini
│   └── utils/
│       ├── logger.py
│       ├── qt_signals.py          # 커스텀 시그널 정의(필요 시)
│       └── types.py               # TypedDict/DTO
├── tests/
│   ├── test_models/
│   │   ├── test_card_transaction_model.py
│   │   └── test_taxpayer_status_model.py
│   ├── test_services/
│   │   ├── test_vat_service.py
│   │   └── test_report_service.py
│   └── test_repositories/
│       ├── test_card_repository.py
│       └── test_taxpayer_repository.py
├── resources/                     # 아이콘, qss, qrc 등
│   ├── icons/
│   └── styles/
├── README.md
└── requirements.txt

```

### Data Flow & Communication Patterns

  - **Client-Server Communication**: UI는 Business Logic을 클라이언트로, Business Logic은 Data Access와 API Integration을 서버로 취급합니다. 요청/응답 패턴을 사용하여 데이터를 주고받습니다.
  - **Database Interaction**: PRD 요구사항 및 Tech Stack에 따라 SQLAlchemy (ORM)를 사용하여 데이터베이스와 상호작용합니다. 이를 통해 데이터베이스 스키마 관리 및 CRUD 작업을 객체 지향적으로 처리합니다. connection pooling을 통해 데이터베이스 연결을 효율적으로 관리합니다.
  - **External Service Integration**: `requests` 라이브러리를 사용하여 국세청 API를 호출하고, JSON 형식으로 데이터를 주고받습니다. API 호출 시 예외 처리를 통해 안정성을 확보합니다.
  - **Real-time Communication**: 실시간 통신 기능은 필요하지 않습니다.
  - **Data Synchronization**: 데이터베이스와 API 데이터 간의 동기화는 필요하지 않습니다.

## 4. Performance & Optimization Strategy

  - 데이터베이스 쿼리 최적화: 인덱스 활용, 불필요한 데이터 조회 최소화
  - 메모리 관리 최적화: 대용량 데이터 처리 시 메모리 누수 방지, 필요한 데이터만 로딩
  - UI 렌더링 최적화: 불필요한 UI 업데이트 최소화, 비동기 처리 활용
  - 멀티스레딩 활용: 시간이 오래 걸리는 작업(예: 엑셀 파일 로딩, API 호출)은 별도 스레드에서 처리하여 UI 응답성 유지

## 5. Implementation Roadmap & Milestones

### Phase 1: Foundation (MVP Implementation)

  - **Core Infrastructure**: Python, PySide6, SQLite 개발 환경 구축, 기본 UI 구성
  - **Essential Features**: 엑셀 파일 가져오기, 데이터베이스 저장, 카드 내역 조회 기능 구현
  - **Basic Security**: 데이터베이스 암호화 기능 구현 (선택 사항)
  - **Development Setup**: 개발 환경 설정, Git 저장소 생성
  - **Timeline**: 4주

### Phase 2: Feature Enhancement

  - **Advanced Features**: 사용자 정보 등록, 사업자 상태 조회 및 관리 (변경 이력 포함), 부가세 제외 대상 거래 관리, 전자 매체 파일 생성 기능 구현
  - **Performance Optimization**: 데이터베이스 쿼리 최적화, UI 렌더링 최적화
  - **Enhanced Security**: API 연동 보안 강화, 개인 정보 보호 강화
  - **Monitoring Implementation**: 로깅 시스템 구축, 오류 발생 시 알림 기능 구현
  - **Timeline**: 6주

## 6. Risk Assessment & Mitigation Strategies

### Technical Risk Analysis

  - **Technology Risks**: PySide6 사용 경험 부족으로 인한 UI 개발 지연 가능성
      - **Mitigation Strategies**: PySide6 관련 문서 및 예제 학습, 스터디 그룹 운영
  - **Performance Risks**: 대용량 엑셀 파일 처리 시 성능 저하 가능성
      - **Mitigation Strategies**: 데이터베이스 인덱스 활용, 메모리 관리 최적화
  - **Security Risks**: 국세청 API 연동 시 보안 취약점 발생 가능성
      - **Mitigation Strategies**: API 보안 가이드라인 준수, 데이터 암호화 적용
  - **Integration Risks**: 국세청 API 변경 시 프로그램 수정 필요성
      - **Mitigation Strategies**: API 변경 사항 모니터링, API 변경에 유연하게 대응할 수 있는 코드 구조 설계

### Project Delivery Risks

  - **Timeline Risks**: 기능 개발 지연으로 인한 프로젝트 일정 지연 가능성
      - **Contingency Plans**: 우선순위가 낮은 기능 제외, 개발 인력 추가 투입
  - **Resource Risks**: 개발 인력 부족으로 인한 프로젝트 진행 어려움
      - **Contingency Plans**: 외부 개발 인력 활용, 기능 개발 범위 축소
  - **Quality Risks**: 코드 품질 저하로 인한 프로그램 오류 발생 가능성
      - **Contingency Plans**: 코드 리뷰 실시, 단위 테스트 및 통합 테스트 강화
  - **Deployment Risks**: 배포 환경 문제로 인한 프로그램 배포 지연 가능성
      - **Contingency Plans**: 배포 환경 사전 점검, 자동 배포 시스템 구축