# 부가세 도우미 (VAT FileMaker)

개인 사업자를 위한 부가세 신고 도우미 프로그램입니다. PySide6-Fluent-Widgets를 사용하여 개발된 데스크톱 애플리케이션으로, 엑셀 카드 사용 내역을 관리하고 부가세 신고를 위한 전자 매체 파일을 생성할 수 있습니다.

## 🚀 주요 기능

### 현재 구현된 기능

#### 기본 인프라
- **FluentWindow 스타일 메인 윈도우**: PySide6-Fluent-Widgets 기반의 세련된 UI
- **네비게이션 메뉴**: 홈, 사업자 정보 관리, 카드사 정보 관리, 카드 정보 관리, 공통코드 관리, 거래처정보 관리, 카드사용내역 등록, 설정 페이지
- **홈 페이지**: 환영 메시지 및 주요 기능 버튼
- **사용자 알림**: InfoBar를 사용한 사용자 친화적 알림 시스템
- **환경 변수 관리**: `python-dotenv`를 사용한 설정 파일 관리

#### 데이터베이스 관리
- **SQLite 데이터베이스**: SQLAlchemy ORM을 사용한 데이터베이스 관리
- **테이블 관리**: 사업자정보, 카드사정보, 카드정보, 공통코드, 거래처정보, 카드사용내역 테이블 지원
- **자동 마이그레이션**: SQL 스크립트 기반 테이블 생성 및 인덱스 관리

#### 사업자 정보 관리
- **사업자 정보 등록/수정/조회/삭제**: 사업자등록번호를 기본 키로 사용
- **사업자 정보 검색**: 사업자명, 대표자명, 업태로 검색 가능
- **데이터 검증**: 필수 필드 검사 및 형식 검증

#### 카드사 정보 관리
- **카드사 정보 등록/수정/조회/삭제**: 카드사 코드(3자리), 한글명, 영문명 관리
- **카드사 정보 검색**: 카드사 코드 또는 명칭으로 검색 가능
- **카드사 코드 유효성 검사**: 3자리 코드 형식 검증

#### 카드 정보 관리
- **카드 정보 등록/수정/조회/삭제**: 카드번호, 카드명, 카드유형, 카드사 연동
- **카드번호 암호화**: Fernet 대칭 키 암호화를 사용한 카드번호 보안 저장
- **카드 정보 검색**: 카드명, 카드사로 검색 가능
- **카드사 콤보**: "선택" 항목을 포함한 카드사 선택 인터페이스

#### 공통코드 관리
- **공통코드 등록/수정/조회/삭제**: 복합 키(code_group, code)를 사용한 코드 관리
- **코드 그룹별 관리**: 코드 그룹별 코드 목록 조회 및 정렬
- **코드 검색**: 코드 그룹, 코드, 코드명, 코드약어명으로 검색 가능
- **사용 여부 관리**: 활성/비활성 코드 관리
- **정렬 순서 관리**: 코드 정렬 순서 설정 지원

#### 거래처정보 관리
- **거래처정보 등록/수정/조회/삭제**: 사업자등록번호(UNIQUE), 거래처명, 과세유형, 사업자 상태 관리
- **공통코드 연동**: 과세유형 및 사업자 상태를 공통코드 테이블과 연동
- **코드약어 표시**: 공통코드의 코드약어(code_abbr)를 콤보박스에 표시
- **거래처정보 검색**: 사업자등록번호, 거래처명으로 검색 가능
- **상태 업데이트일 관리**: 사업자 상태 업데이트 날짜 기록

#### 카드사용내역 등록
- **엑셀 파일 업로드**: 카드사 홈페이지에서 다운받은 엑셀 파일 업로드
- **자동 컬럼 매핑**: 다양한 엑셀 형식의 컬럼명 자동 인식 및 매핑
- **데이터 미리보기**: 엑셀 데이터를 TableView에서 확인 후 선택적 등록
- **다중 행 선택**: 전체 선택/선택 해제 기능으로 일괄 등록 지원
- **데이터 파싱**: 날짜, 금액, 취소여부, 사업자번호 등 자동 파싱 및 검증
- **카드사별 처리**: 카드사 선택에 따른 데이터 분류 및 저장

#### 보안 기능
- **카드번호 암호화**: `cryptography` 패키지의 Fernet을 사용한 대칭 키 암호화
- **암호화 키 관리**: `.env` 파일을 통한 암호화 키 관리
- **자동 암호화/복호화**: 저장 시 자동 암호화, 조회 시 자동 복호화

### 향후 구현 예정 기능
- **카드 내역 데이터 관리**: 카드 사용 내역 조회, 수정, 삭제 기능
- **사업자 상태 조회**: 국세청 API를 통한 사업자 상태 확인
- **부가세 제외 대상 관리**: 사업자 상태에 따른 자동 제외 처리
- **전자 매체 파일 생성**: 부가세 신고용 전자 파일 생성
- **통계 및 리포트**: 거래 내역 분석 및 리포트 생성

## 🛠️ 기술 스택

- **언어**: Python 3.13+
- **GUI 프레임워크**: PySide6 + PySide6-Fluent-Widgets
- **데이터베이스**: SQLite + SQLAlchemy (ORM)
- **엑셀 처리**: pandas, openpyxl
- **API 통신**: requests
- **로깅**: loguru
- **테스트**: pytest
- **패키지 관리**: uv
- **암호화**: cryptography (Fernet)
- **환경 변수 관리**: python-dotenv

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/nawhizz/vat-filemaker.git
cd vat-filemaker
```

### 2. 의존성 설치
```bash
uv sync
```

### 3. 애플리케이션 실행
```bash
uv run python main.py
```

## 🏗️ 프로젝트 구조

```
vat-filemaker/
├── main.py                 # 애플리케이션 진입점
├── pyproject.toml          # 프로젝트 설정 및 의존성
├── README.md              # 프로젝트 문서
├── app/                   # 애플리케이션 코드
│   ├── views/            # UI 계층 (PySide6 위젯)
│   │   ├── main_window.py # 메인 윈도우 구현
│   │   ├── business_registration_view.py # 사업자 정보 관리 UI
│   │   ├── card_company_view.py # 카드사 정보 관리 UI
│   │   ├── card_view.py # 카드 정보 관리 UI
│   │   ├── common_code_view.py # 공통코드 관리 UI
│   │   ├── vendor_view.py # 거래처정보 관리 UI
│   │   └── card_transaction_view.py # 카드사용내역 등록 UI
│   ├── models/           # 데이터 모델 (QAbstractItemModel)
│   │   ├── card_company_model.py # 카드사 정보 모델
│   │   ├── card_model.py # 카드 정보 모델
│   │   ├── common_code_model.py # 공통코드 모델
│   │   ├── vendor_model.py # 거래처정보 모델
│   │   └── card_transaction_model.py # 카드사용내역 모델
│   ├── services/         # 비즈니스 로직
│   │   ├── business_service.py # 사업자 정보 서비스
│   │   ├── card_company_service.py # 카드사 정보 서비스
│   │   ├── card_service.py # 카드 정보 서비스 (암호화 포함)
│   │   ├── common_code_service.py # 공통코드 서비스
│   │   ├── vendor_service.py # 거래처정보 서비스
│   │   └── card_transaction_service.py # 카드사용내역 서비스
│   ├── repositories/     # 데이터 접근 계층
│   │   ├── database.py # 데이터베이스 초기화
│   │   ├── schema.py # SQLAlchemy ORM 모델
│   │   ├── business_repository.py # 사업자 정보 Repository
│   │   ├── card_company_repository.py # 카드사 정보 Repository
│   │   ├── card_repository.py # 카드 정보 Repository
│   │   ├── common_code_repository.py # 공통코드 Repository
│   │   ├── vendor_repository.py # 거래처정보 Repository
│   │   ├── card_transaction_repository.py # 카드사용내역 Repository
│   │   └── sql/ # SQL 스크립트 파일
│   │       ├── business_info.sql
│   │       ├── card_company_info.sql
│   │       ├── card_info.sql
│   │       ├── common_code.sql
│   │       ├── vendor_info.sql
│   │       └── card_transaction.sql
│   ├── api/             # 외부 API 연동
│   ├── adapters/        # 입출력 어댑터
│   ├── config/          # 설정 관리
│   │   └── settings.py # 환경 변수 설정 관리
│   └── utils/           # 유틸리티 함수
│       ├── crypto.py # 암호화/복호화 유틸리티
│       ├── excel_reader.py # 엑셀 파일 읽기 유틸리티
│       ├── font.py # 폰트 관리 유틸리티
│       └── logger.py # 로깅 설정
├── docs/                # 프로젝트 문서
│   ├── prd.md          # 제품 요구사항 문서
│   ├── trd.md          # 기술 요구사항 문서
│   └── Code Guideline.md # 코딩 가이드라인
├── tests/               # 단위 테스트
└── resources/           # 리소스 파일 (아이콘, 스타일)
```

## 🎨 UI 스크린샷

### 메인 윈도우
- **윈도우 크기**: 1024x768
- **스타일**: Fluent Design
- **네비게이션**: 사이드바 네비게이션 메뉴

### 홈 페이지
- 환영 메시지
- 프로그램 소개
- 주요 기능 버튼 (엑셀 파일 업로드, 사업자 상태 조회)

## 🏛️ 아키텍처

### MVA (Model-View-Architecture) 패턴 적용
- **View**: PySide6 위젯을 사용한 UI 계층
- **Model**: QAbstractItemModel을 상속받은 데이터 모델
- **Service**: 비즈니스 로직 처리
- **Repository**: 데이터 접근 계층 (SQLAlchemy ORM)

### 레이어 분리
- **UI Layer**: 사용자 인터페이스 및 상호작용
- **Business Logic Layer**: 핵심 비즈니스 로직
- **Data Access Layer**: 데이터베이스 연동
- **API Integration Layer**: 외부 API 연동

## 📋 개발 가이드라인

### 코딩 스타일
- **PEP 8 준수**: Python 표준 코딩 스타일 적용
- **타입 힌팅**: 모든 함수와 메서드에 타입 힌팅 필수
- **한국어 주석**: 코드 가독성을 위한 한국어 주석 작성
- **Docstring**: Google 또는 reST 형식의 문서화

### 네이밍 규칙
- **변수/함수**: snake_case 사용
- **클래스**: PascalCase 사용
- **상수**: UPPER_CASE 사용
- **Boolean 변수**: is, has, can으로 시작

### 에러 처리
- 모든 함수에서 예외 상황 고려
- loguru를 사용한 구조화된 로깅
- 사용자 친화적 에러 메시지 제공

## 🧪 테스트

```bash
# 모든 테스트 실행
uv run pytest

# 특정 테스트 실행
uv run pytest tests/test_services/

# 커버리지 포함 테스트
uv run pytest --cov=app
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 연락처

프로젝트 링크: [https://github.com/nawhizz/vat-filemaker](https://github.com/nawhizz/vat-filemaker)

## 🔄 버전 히스토리

### v0.3.0 (2025-01-27)
- **feat**: 카드사용내역 등록 기능 추가
  - 엑셀 파일 업로드 및 파싱 기능
  - 자동 컬럼 매핑 및 데이터 파싱
  - 다중 행 선택 및 일괄 등록 기능
  - 카드사별 데이터 분류 및 저장
- **feat**: 엑셀 파일 읽기 유틸리티 추가
  - 다양한 엑셀 형식 지원
  - 날짜, 금액, 취소여부, 사업자번호 자동 파싱
  - 유연한 컬럼명 매핑 시스템
- **feat**: 카드사용내역 테이블 및 DB 처리 추가
  - card_transaction 테이블 생성
  - Repository, Service, Model 계층 구현
- **feat**: 카드번호 형식 자동 적용
  - Amex, Diners Club, Standard 카드 형식 자동 인식
  - 실시간 입력 형식 적용 및 길이 검증
  - 마스킹된 카드번호 컬럼 추가

### v0.2.0 (2025-01-27)
- **feat**: 공통코드 관리 기능 추가
  - 복합 키(code_group, code) 지원
  - 코드 그룹별 조회 및 검색 기능
  - 코드약어(code_abbr) 지원
- **feat**: 거래처정보 관리 기능 추가
  - 과세유형 및 사업자 상태를 공통코드와 연동
  - 코드약어 표시 및 코드값 저장
  - 사업자등록번호 유효성 검사
- **feat**: 카드정보 관리 화면 개선
  - 카드사 콤보에 '선택' 항목 추가
  - 신규 입력 시 '선택' 항목이 기본으로 표시

### v0.1.1 (2025-01-27)
- **feat**: 카드번호 암호화 기능 추가
  - Fernet 대칭 키 암호화 사용
  - .env 파일을 통한 암호화 키 관리
  - 저장 시 자동 암호화, 조회 시 자동 복호화
- **feat**: 환경 변수 관리 시스템 구축
  - python-dotenv 패키지 사용
  - .env 파일 기반 설정 관리

### v0.1.0 (2025-01-27)
- **feat**: 사업자 정보 관리 기능 구현
  - 사업자 정보 CRUD 기능
  - 사업자 정보 검색 기능
- **feat**: 카드사 정보 관리 기능 구현
  - 카드사 정보 CRUD 기능
  - 카드사 정보 검색 기능
- **feat**: 카드 정보 관리 기능 구현
  - 카드 정보 CRUD 기능
  - 카드사 연동 및 검색 기능
- **feat**: PySide6-Fluent-Widgets 기반 메인 윈도우 구현
- **feat**: 네비게이션 메뉴 및 홈 페이지 UI 구현
- **feat**: 윈도우 크기 1024x768 설정
- **feat**: MVA 아키텍처 패턴 적용
- **feat**: 한국어 주석 및 타입 힌팅 적용
- **feat**: SQLite + SQLAlchemy 데이터베이스 연동

---

## 📚 참고 문서

- [PySide6 공식 문서](https://doc.qt.io/qtforpython/)
- [PySide6-Fluent-Widgets 문서](https://qfluentwidgets.com/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [pandas 문서](https://pandas.pydata.org/docs/)

## 🔗 참고 사이트트

- [카드사 금융결제원 표준 코드](https://faq.portone.io/53589280-bbc9-4fab-938d-93257d452216)
- [국세청_사업자등록정보 진위확인 및 상태조회 서비스](https://www.data.go.kr/data/15081808/openapi.do)

---

## 🗄️ 데이터베이스 스키마

### 테이블 목록
- **business_info**: 사업자 정보 테이블
- **card_company_info**: 카드사 정보 테이블
- **card_info**: 카드 정보 테이블 (카드번호 암호화)
- **common_code**: 공통코드 테이블 (복합 키: code_group, code)
- **vendor_info**: 거래처정보 테이블
- **card_transaction**: 카드사용내역 테이블

### 공통코드 그룹
- **tax_type**: 과세유형 코드
- **business_status**: 사업자 상태 코드

자세한 스키마 정보는 `docs/Database.md`를 참고하세요.

## 🔐 보안

### 카드번호 암호화
- 카드번호는 Fernet 대칭 키 암호화를 사용하여 저장됩니다.
- 암호화 키는 `.env` 파일의 `ENCRYPTION_KEY` 환경 변수에서 관리됩니다.
- 저장 시 자동 암호화, 조회 시 자동 복호화가 수행됩니다.

### 환경 변수 설정
`.env` 파일을 프로젝트 루트에 생성하여 다음 변수들을 설정하세요:
```
DATABASE_PATH=data/vat_filemaker.db
ENCRYPTION_KEY=your-encryption-key-here
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
DEBUG=False
DEV_MODE=False
```

## 📊 주요 기능 상세

### 공통코드 관리
- 코드 그룹별로 코드를 관리할 수 있습니다.
- 코드명(code_name)과 코드약어(code_abbr)를 모두 저장할 수 있습니다.
- 정렬 순서(sort_order)를 지정하여 코드 목록 순서를 제어할 수 있습니다.
- 사용 여부(is_active)를 통해 활성/비활성 코드를 관리할 수 있습니다.

### 거래처정보 관리
- 거래처의 사업자등록번호, 거래처명, 과세유형, 사업자 상태를 관리합니다.
- 과세유형과 사업자 상태는 공통코드 테이블과 연동되어 코드약어가 표시됩니다.
- 사업자 상태 업데이트일을 기록하여 상태 변경 이력을 관리할 수 있습니다.

### 카드사용내역 등록
- 카드사 홈페이지에서 다운받은 엑셀 파일을 업로드하여 카드사용내역을 일괄 등록할 수 있습니다.
- 다양한 엑셀 형식을 자동으로 인식하고 매핑합니다.
- 거래일자, 금액, 거래처명, 사업자번호, 승인번호 등을 자동으로 파싱합니다.
- 취소 거래는 "취소", "cancel" 등의 키워드로 자동 인식됩니다.
- TableView에서 데이터를 미리 확인한 후 선택적으로 등록할 수 있습니다.

---

**개발 상태**: 🚧 개발 중 (MVP 단계)

**다음 단계**: 카드 내역 데이터 조회/수정/삭제 기능 및 부가세 제외 대상 관리 기능 구현 예정
