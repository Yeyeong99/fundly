# 금감원 API 사용해서 데이터 받아오기
import requests
import json

from django.conf import settings

# 요청 url
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

# 금융회사 : companySearch >> max_page_no=1

# 데이터 불러오기 >> 금융 회사
def get_comp_data(topFinGrpNo):
    # 1. 최대 페이지 수 받기
    # 요청 URL
    API_URL = BASE_URL + 'companySearch.json'
    params = {
        'auth': settings.FINANCE_API_KEY,
        'topFinGrpNo': topFinGrpNo,    # 020000, 030300 두개만 해도 될 듯 >> 정기 예금, 적금 상품이 이것 밖에 없다.
        'pageNo': 1
    }
    
    response = requests.get(API_URL, params=params).json()
    max_page_no = response['result']['max_page_no']
    companies = []
    
    # 2. 최대 페이지 수 만큼 반복해서 회사 수 받기
    for n in range(1, max_page_no+1):
        API_URL = BASE_URL + 'companySearch.json'
        params = {
            'auth': settings.FINANCE_API_KEY,
            'topFinGrpNo': topFinGrpNo,    # 020000, 030300 두개만 해도 될 듯 >> 정기 예금, 적금 상품이 이것 밖에 없다.
            'pageNo': n
        }
        response = requests.get(API_URL, params=params).json()

        company = response['result']['baseList']
        
        companies.extend(company)

    extracted_companies = []
    
    for company in companies:
        # 금융회사 권역 코드 넣어주기
        company_dict = {'company_type': topFinGrpNo}
        for key in company:
            if key in ['fin_co_no', 'kor_co_nm', 'homp_url', 'cal_tel']:
                company_dict[key] = company.get(key, '')
                
        extracted_companies.append(company_dict)

    return extracted_companies


# fixture 만들기 >> 회사
def create_company_data():

    all_extracted_companies = []

    for topFinGrpNo in ['020000', '030300']:
        extracted_companies = get_comp_data(topFinGrpNo)
        all_extracted_companies.extend(extracted_companies)

    company_data = []
    
    # 키값 바꿔주기
    for company in all_extracted_companies:

        fixture_fields = {}

        for key in company.keys():
            if key == 'fin_co_no':
                fixture_fields['company_code'] = company[key]
            
            elif key == 'kor_co_nm':
                fixture_fields['company_name'] = company[key]

            elif key == 'homp_url':
                fixture_fields['homepage_url'] = company[key]

            elif key == 'cal_tel':
                fixture_fields['phone_number'] = company[key]
            
            else:
                fixture_fields[key] = company[key]

        company_data.append(fixture_fields)

    company_result_string = json.dumps(company_data)
    company_result = json.loads(company_result_string)

    print(f'총 {len(company_data)}개의 fixture.financialcompany 항목이 저장되었습니다.')

    return company_result

    
# if __name__ == "__main__":
#     company_result = create_fixture_company()
#     print(company_result[:5])
