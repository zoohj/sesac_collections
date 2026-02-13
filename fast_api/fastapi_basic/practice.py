from pydantic import BaseModel

class Address(BaseModel):
    city: str
    zip_code: str

class Company(BaseModel):
    name: str
    # Address 모델을 필드 형식으로 사용
    address: Address

# 중첩된 형태의 데이터 입력
company_info = {
    "name": "기술연구소",
    "addreses": {
        "city": "서울",
        "zip_code": "12345"
    }
}

company = Company(**company_info)
# 하위 객체의 속성에 접근
print(company.address.city)

