### 1. 공통 코드드 (CommonCode)
```
common_code
├── code_group: String (PK)		# 코드 그룹명
├── code: String (PK)      		# 코드 값
├── code_name: String          	# 코드명
├── sort_order: INTEGER       	# 정렬 순서
├── is_active: BOOLEAN 		   	# 사용 여부
├── description: TEXT 		   	# 비고
├── created_at: DateTime       	# 생성 시간
└── updated_at: DateTime       	# 최종 수정 시간
```


### 2. 사업자 정보 (BusinessInfo)
```
business_info
├── business_number: String       # 사업자등록번호
├── business_name: String         # 사업자명
├── owner_name: String            # 대표자명
├── owner_resident_number         # 대표자주민등록번호
├── business_type: String         # 업태
├── business_category: String     # 종목
├── address: String               # 주소
├── phone_number: String          # 전화번호
├── email: String                 # 이메일
├── created_at: DateTime          # 생성 시간
└── updated_at: DateTime          # 최종 수정 시간
```


### 3. 카드사 정보 (CardCompanyInfo)
```
card_company_info
├── id: Integer                   # 자동 생성 기본 키
├── card_company_code: String     # 카드사 코드 (금융사 고유코드)
├── card_company_name: String     # 카드사 한글명
├── card_company_name_en: String  # 카드사 영문명
├── created_at: DateTime          # 생성 시간
└── updated_at: DateTime          # 최종 수정 시간
```
※ 부가세 신고시 카드사에 다운받는 카드사용내역에 카드번호는 마스킹되어 있음
   따라서, 카드사 마다 어떤 형식으로 마스킹되는지 관리가 필요함


### 4. 카드 정보 (CardInfo)
```
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
※ 부가세 신고시 카드사에 다운받는 카드사용내역의 마스킹된 카드번호 별도 관리 필요
   따라서, 카드사 정보의 카드 마스킹 정보로 카드번호 마스킹해서 별도 컬럼에 관리

**카드번호로 카드번호 형식 구분 방법**
| 카드사        | 카드번호 자리수 | 형식                | 시작 번호(BIN)         |
|--------------|----------------|--------------------|----------------------|
| 아멕스       | 15자리         | xxxx-xxxxxx-xxxxx   | 34, 37               |
| 다이너스클럽 | 14자리         | xxxx-xxxxxx-xxxx    | 36, 3616 등          |
| 일반카드     | 16자리         | xxxx-xxxx-xxxx-xxxx | 4(비자), 5(마스터) 등 |


### 5. 거래처 정보 (VendorInfo)
```
vendor_info
├── id: Integer (PK)           		   # 자동 생성 기본 키
├── business_number: String (UNIQUE)   # 거래처 사업자등록번호
├── vendor_name: String        		   # 거래처명
├── tax_type: String          		   # 과세유형 (01:일반과세자, 02:간이과세자, 03:과세특례자, 04: 면세사업자 등등)
├── business_status: String 		      # 사업자 상태 (01:계속사업자, 02:휴업, 03:폐업 등)	
├── status_updated_at: DateTime 	      # 상태 업데이트 날짜
├── created_at: DateTime       		   # 생성 시간
└── updated_at: DateTime       		   # 최종 수정 시간
```


- [카드사 금융결제원 표준 코드](https://faq.portone.io/53589280-bbc9-4fab-938d-93257d452216)
- [국세청_사업자등록정보 진위확인 및 상태조회 서비스](https://www.data.go.kr/data/15081808/openapi.do)