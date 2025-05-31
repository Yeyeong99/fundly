from datetime import datetime

ASSET_RANGE_MAP = {
    "1,000만원 미만": 500,
    "1,000만원 이상 3,000만원 미만": 2000,
    "3,000만원 이상 5,000만원 미만": 4000,
    "5,000만원 이상 1억 미만": 7500,
    "1억 이상": 12000,
}

SALARY_RANGE_MAP = {
    "100만원 미만": 50,
    "100만원 이상 200만원 미만": 150,
    "200만원 이상 300만원 미만": 250,
    "300만원 이상 400만원 미만": 350,
    "400만원 이상 500만원 미만": 450,
    "500만원 이상": 600,
}

WORK_TYPE_CATEGORIES = ['직장인', '공무원', '군인', '전문직', '학생', '취업준비생',
        '자영업자', '프리랜서', '예술가/창작자', '주부', '은퇴자', '무직']

# 생년월일 나이로 변경
def calculate_age(birth_date_str):
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    print(birth_date)
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# 재직여부 원핫인코딩
def encoding_work_type(input_type: str) -> list:
    return [1 if input_type == wt else 0 for wt in WORK_TYPE_CATEGORIES]

# 사용자 정보 파싱하기 >> 벡터화 하기 위해서
def parse_user_input(input_data):
    birth_date_str = input_data.get("birth_date")
    print(f'가져와진 생년월일 : {birth_date_str}')
    if not birth_date_str:
        raise ValueError("birth_date가 누락되었습니다.")

    age = calculate_age(birth_date_str)
    assets = ASSET_RANGE_MAP[input_data["assets"]]
    salary = SALARY_RANGE_MAP[input_data["salary"]]
    work_vector = encoding_work_type(input_data["work_type"])
    
    username = input_data.get("username")
    if hasattr(username, "email"):  # User 객체인 경우
        username = username.email
    else:
        username = str(username)

    return {
        "username": username,
        "age": age,
        "assets": assets,
        "salary": salary,
        "work_type": work_vector,
        "goal": input_data["goal"],
    }
