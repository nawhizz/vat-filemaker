**Google AI Studio**
```
<prd.md><trd.md>
첨부한 trd가 prd의 내용을 충실히 반영했는지, 검토하고 개선해줘.
개선해야 할 포인트를 간단하게 설명한 뒤, 모두 설명하고나서 완성본을 만들어줘.
```

**Google AI Studio**
```
<prd.md><trd.md>
첨부한 prd, trd를 참조해서, 바이브코딩을 위한 단계적 태스크를 작성해줘.
```

**Cursor**
```
다음 카드사 정보 테이블을 사업자 정보 테이블(business_info)을 참조해서 DB 처리 추가해줘.

card_company_info
├── id: Integer                   # 자동 생성 기본 키
├── card_company_code: String     # 카드사 코드 (금융사 고유코드)
├── card_company_name: String     # 카드사 한글명
├── card_company_name_en: String  # 카드사 영문명
├── created_at: DateTime          # 생성 시간
└── updated_at: DateTime          # 최종 수정 시간
```

```
<NH멤버스 캡처 화면면>
첨부한 파일을 참조해서 카드사 정보(card_company_info)를 등록하는 화면 작성해줘.
```

```
카드사 정보의 TableView를 다음의 QFluentWidgets 의 TableView를 참조해서 적용해줘.

@https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/table_view/demo.py
```

```
지금 까지 수정 또는 추가된 파일을 GitHub https://github.com/nawhizz/vat-filemaker.git 에 commit 해줘.
```

**ChatGPT**
```
다음은 카드 정보 테이블의 컬럼 한글명이야. 테이블과 컬럼의 영문명을 작성해줘.
영문 컬럼명 작성시에 참조 테이블 (카드사 정보)를 참조해.

**카드 정보**
자동 생성 기본 키
카드번호(암호화)
카드명
카드유형
카드사 ID (외래 키)
사용여부
생성 시간
최종 수정 시간

<참조 테이블>
card_company_info
├── id: Integer (PK)           # 자동 생성 기본 키
├── company_code: String       # 카드사 코드
├── company_name: String       # 카드사 한글명 
├── company_name_en: String    # 카드사 영문명 
├── created_at: DateTime       # 생성 시간
└── updated_at: DateTime       # 최종 수정 시간
```

**Cursor**
```
다음은 카드정보 테이블 생성을 위한 컬럼 정보야.
repositories\sql 폴더에 테이블 생성 스크립트 파일 작성해줘.

card_info
├── id: Integer (PK)                      # 자동 생성 기본 키
├── card_number: String                   # 카드번호(암호화)
├── card_name: String                     # 카드명
├── card_type: String                     # 카드유형
├── card_company_id: Integer (FK)         # 카드사 ID (외래 키)
├── is_active: Boolean                    # 사용여부
├── created_at: DateTime                  # 생성 시간
└── updated_at: DateTime                  # 최종 수정 시간
```

```
@card_info.sql @card_company_info.sql 
카드사정보 테이블을 참조해서, 카드정보 테이블에 대한 DB 처리를 추가해줘.
```

```
@card_company_view.py
 카드사정보 화면을 참조해서, 카드정보 등록하는 화면 작성해줘.
```

**ChatGPT**
```
다음은 카드사용내역에 포함되는 거래처의 정보를 관리하기 위한 거래처정보 테이블의 한글명이야. 영문 테이블명과 컬럼명을 작성해줘.
영문 컬럼명 작성시에는 참조 테이블(사업자 정보)를 참조해.

**거래처처 정보**
사업자등록번호
거래처명
과세유형코드
사업자 상태 (정상/폐업/휴업 등)
상태 업데이트 날짜
생성 시간
최종 수정 시간

<참조 테이블>
business_info
├── business_number: String    # 사업자등록번호
├── business_name: String      # 사업자명
├── owner_name: String         # 대표자명
├── owner_resident_number      # 대표자주민등록번호
├── business_type: String      # 업태
├── business_category: String  # 종목
├── address: String            # 주소
├── phone_number: String       # 전화번호
├── email: String              # 이메일
├── created_at: DateTime       # 생성 시간
└── updated_at: DateTime       # 최종 수정 시간
```

**ChatGPT**
```
위의 tax_type 같은 것은 코드에 따른 코드명 관리가 필요한데, 이렇게 코드에 따른 코드 정보를 관리하는 테이블이 별도로 필요할 것 같어. 이 공통코드 테이블 설계를 해줘.
```

**Cursor**
```
다음은 공통코드 테이블 생성을 위한 컬럼 정보야.
repositories\sql 폴더에 테이블 생성 스크립트 파일 작성해줘.

common_code
├── code_group: String (PK)		# 코드 그룹명
├── code: String (PK)      		# 코드 값
├── code_name: String        	# 코드명
├── code_abbr: String        	# 코드약어명
├── sort_order: INTEGER     	# 정렬 순서
├── is_active: BOOLEAN 			# 사용 여부
├── description: TEXT 			# 비고
├── created_at: DateTime       	# 생성 시간
└── updated_at: DateTime       	# 최종 수정 시간
```

**Cursor**
```
@common_code.sql @ccard_company_service.py 
카드사정보 테이블을 참조해서, 공통코드 테이블에 대한 DB 처리를 추가해줘.
```

**Cursor**
```
다음은 거래처정보 테이블 생성을 위한 컬럼 정보야.
repositories\sql 폴더에 테이블 생성 스크립트 파일 작성해줘.

vendor_info
├── id: Integer (PK)           		   # 자동 생성 기본 키
├── business_number: String (UNIQUE)   # 거래처 사업자등록번호
├── vendor_name: String        		   # 거래처명
├── tax_type: String          		   # 과세유형 (01:일반과세자, 02:간이과세자, 03:과세특례자, 04: 면세사업자 등등)
├── business_status: String 		   # 사업자 상태 (01:계속사업자, 02:휴업, 03:폐업 등)	
├── status_updated_at: DateTime 	   # 상태 업데이트 날짜
├── created_at: DateTime       		   # 생성 시간
└── updated_at: DateTime       		   # 최종 수정 시간
```

**Cursor**
```
@vendor_info.sql @ccard_company_service.py 
카드사정보 테이블을 참조해서, 거래처정보 테이블에 대한 DB 처리를 추가해줘.
tax_type, business_status 컬럼의 코드에 대한 코드명은 common_code 테이블에서 가져올수 있어.
```