### 1. 사업자 정보 (BusinessInfo)
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

### 2. 카드사 정보 (CardCompanyInfo)
```
card_company_info
├── id: Integer                   # 자동 생성 기본 키
├── card_company_code: String     # 카드사 코드 (금융사 고유코드)
├── card_company_name: String     # 카드사 한글명
├── card_company_name_en: String  # 카드사 영문명
├── created_at: DateTime          # 생성 시간
└── updated_at: DateTime          # 최종 수정 시간
```

- [카드사 금융결제원 표준 코드](https://faq.portone.io/53589280-bbc9-4fab-938d-93257d452216)