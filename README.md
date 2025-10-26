# 부가세 도우미 (VAT FileMaker)

개인 사업자를 위한 부가세 신고 도우미 프로그램입니다. PySide6-Fluent-Widgets를 사용하여 개발된 데스크톱 애플리케이션으로, 엑셀 카드 사용 내역을 관리하고 부가세 신고를 위한 전자 매체 파일을 생성할 수 있습니다.

## 🚀 주요 기능

### 현재 구현된 기능
- **FluentWindow 스타일 메인 윈도우**: PySide6-Fluent-Widgets 기반의 세련된 UI
- **네비게이션 메뉴**: 홈, 카드 내역, 사업자 관리, 부가세 신고, 설정 페이지
- **홈 페이지**: 환영 메시지 및 주요 기능 버튼
- **사용자 알림**: InfoBar를 사용한 사용자 친화적 알림 시스템

### 향후 구현 예정 기능
- **엑셀 파일 업로드**: 카드사에서 다운받은 엑셀 파일 업로드 및 파싱
- **데이터베이스 저장**: SQLite를 사용한 카드 내역 데이터 저장
- **사업자 상태 조회**: 국세청 API를 통한 사업자 상태 확인
- **부가세 제외 대상 관리**: 사업자 상태에 따른 자동 제외 처리
- **전자 매체 파일 생성**: 부가세 신고용 전자 파일 생성

## 🛠️ 기술 스택

- **언어**: Python 3.13+
- **GUI 프레임워크**: PySide6 + PySide6-Fluent-Widgets
- **데이터베이스**: SQLite + SQLAlchemy (ORM)
- **엑셀 처리**: pandas, openpyxl
- **API 통신**: requests
- **로깅**: loguru
- **테스트**: pytest
- **패키지 관리**: uv

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
│   │   └── main_window.py # 메인 윈도우 구현
│   ├── models/           # 데이터 모델 (QAbstractItemModel)
│   ├── services/         # 비즈니스 로직
│   ├── repositories/     # 데이터 접근 계층
│   ├── api/             # 외부 API 연동
│   ├── adapters/        # 입출력 어댑터
│   ├── config/          # 설정 관리
│   └── utils/           # 유틸리티 함수
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

### v0.1.0 (2025-01-27)
- **feat**: PySide6-Fluent-Widgets 기반 메인 윈도우 구현
- **feat**: 네비게이션 메뉴 및 홈 페이지 UI 구현
- **feat**: 윈도우 크기 1024x768 설정
- **feat**: MVA 아키텍처 패턴 적용
- **feat**: 한국어 주석 및 타입 힌팅 적용

---

## 📚 참고 문서

- [PySide6 공식 문서](https://doc.qt.io/qtforpython/)
- [PySide6-Fluent-Widgets 문서](https://qfluentwidgets.com/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [pandas 문서](https://pandas.pydata.org/docs/)

---

**개발 상태**: 🚧 개발 중 (MVP 단계)

**다음 단계**: 엑셀 파일 업로드 및 데이터베이스 연동 기능 구현 예정
