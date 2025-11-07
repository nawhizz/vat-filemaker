# 폰트 설정 가이드

## 개요

애플리케이션 전체의 폰트는 `app/utils/font.py`에서 중앙 관리됩니다.
모든 폰트 설정은 이 모듈의 유틸리티 함수를 사용하여 일관성을 유지하고 유지보수를 쉽게 합니다.

## 폰트 설정 상수

`app/utils/font.py`에 정의된 상수:

```python
DEFAULT_FONT_FAMILY = "맑은 고딕"        # 기본 폰트 (한글명)
DEFAULT_FONT_FAMILY_EN = "Malgun Gothic" # 기본 폰트 (영문명)
DEFAULT_FONT_SIZE = 9                    # 기본 폰트 크기 (포인트)
```

## 유틸리티 함수

### 1. `get_available_font_family()`
시스템에서 사용 가능한 폰트 패밀리 이름을 반환합니다.

```python
from app.utils.font import get_available_font_family

font_family = get_available_font_family()
# 반환값: "맑은 고딕" 또는 "Malgun Gothic" 또는 시스템 기본 폰트
```

### 2. `get_app_font(size=None)`
애플리케이션 폰트 객체를 생성합니다.

```python
from app.utils.font import get_app_font

# 기본 크기(9pt) 사용
font = get_app_font()

# 사용자 지정 크기
large_font = get_app_font(size=12)
```

### 3. `get_font_stylesheet(size=None)`
전역 폰트 스타일시트 문자열을 생성합니다.

```python
from app.utils.font import get_font_stylesheet

# QApplication에 적용
app.setStyleSheet(get_font_stylesheet())

# 사용자 지정 크기
app.setStyleSheet(get_font_stylesheet(size=10))
```

### 4. `get_table_font_stylesheet(size=None)`
TableView용 폰트 스타일시트 문자열을 생성합니다.

```python
from app.utils.font import get_table_font_stylesheet

# TableView에 적용
table_view.setStyleSheet(get_table_font_stylesheet())

# 사용자 지정 크기
table_view.setStyleSheet(get_table_font_stylesheet(size=10))
```

## 사용 예시

### 메인 애플리케이션 폰트 설정

**`main.py`**:
```python
from app.utils.font import get_app_font, get_font_stylesheet

# 전체 애플리케이션 폰트 설정
app.setFont(get_app_font())
app.setStyleSheet(get_font_stylesheet())
```

### View에서 TableView 폰트 설정

**`app/views/your_view.py`**:
```python
from app.utils.font import get_app_font, get_table_font_stylesheet

# TableView 폰트 설정
table_font = get_app_font()
self.table_view.setFont(table_font)

# 헤더 폰트 설정
header = self.table_view.horizontalHeader()
header.setFont(table_font)

# 스타일시트로 강제 적용 (FluentWidgets 호환)
self.table_view.setStyleSheet(get_table_font_stylesheet())
```

### Model에서 폰트 반환

**`app/models/your_model.py`**:
```python
from app.utils.font import get_app_font

class YourModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._font = get_app_font()
    
    def data(self, index, role):
        # ... 다른 role 처리 ...
        
        if role == Qt.ItemDataRole.FontRole:
            return self._font
        
        return None
    
    def headerData(self, section, orientation, role):
        # ... 다른 role 처리 ...
        
        if role == Qt.ItemDataRole.FontRole:
            return self._font
        
        return None
```

## 폰트 변경 방법

전체 애플리케이션의 폰트를 변경하려면 `app/utils/font.py`의 상수만 수정하면 됩니다:

```python
# app/utils/font.py
DEFAULT_FONT_FAMILY = "나눔고딕"        # 폰트 변경
DEFAULT_FONT_FAMILY_EN = "NanumGothic"
DEFAULT_FONT_SIZE = 10                   # 크기 변경
```

이렇게 하면 모든 곳에서 자동으로 새로운 폰트가 적용됩니다.

## 주의사항

1. **일관성 유지**: 폰트 설정은 반드시 `app/utils/font.py`의 유틸리티 함수를 사용하세요.
2. **직접 설정 금지**: `QFont("맑은 고딕")`처럼 직접 폰트를 생성하지 마세요.
3. **폰트 크기**: 특별한 이유가 없다면 기본 크기(9pt)를 사용하세요.
4. **FluentWidgets**: FluentWidgets의 TableView는 스타일시트를 통한 폰트 적용이 필요합니다.

## 기존 코드 마이그레이션

기존에 직접 폰트를 설정한 코드가 있다면 다음과 같이 변경하세요:

**변경 전**:
```python
from PySide6.QtGui import QFont

font = QFont("맑은 고딕")
font.setPointSize(9)
widget.setFont(font)
```

**변경 후**:
```python
from app.utils.font import get_app_font

widget.setFont(get_app_font())
```

## 참고 파일

폰트 설정 적용 예시:
- `main.py` - 전체 애플리케이션 폰트 설정
- `app/views/vendor_view.py` - TableView 폰트 설정
- `app/models/vendor_model.py` - Model에서 폰트 반환

