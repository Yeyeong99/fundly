import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("ko_KR")

# 기본 설정
num_users = 500
work_types = ['직장인', '학생', '자영업자', '프리랜서', '무직']
product_types = ['D', 'S', 'A']

# 더미 사용자 데이터 생성
users = []
for i in range(num_users):
    username = fake.user_name()
    email = fake.email()
    birth_date = fake.date_of_birth(minimum_age=17, maximum_age=60)
    work_type = random.choice(work_types)
    assets = random.randint(100, 10000)  # 단위: 만원
    salary = random.randint(50, 800)     # 단위: 만원
    users.append({
        "user_id": i + 1,
        "username": username,
        "email": email,
        "birth_date": birth_date,
        "work_type": work_type,
        "assets": assets,
        "salary": salary
    })

# 더미 목표 데이터 생성
goals = []
for user in users:
    for _ in range(random.randint(1, 3)):  # 유저마다 1~3개 목표
        product_type = random.choice(product_types)
        total_target = random.randint(1000, 10000)
        savings_target = total_target if product_type in ['S', 'A'] else 0
        deposit_target = total_target if product_type in ['D', 'A'] else 0
        start_date = fake.date_between(start_date='-2y', end_date='today')
        end_date = start_date + timedelta(days=random.randint(180, 720))
        goals.append({
            "user_id": user["user_id"],
            "goal_name": fake.word() + " 목표",
            "product_type": product_type,
            "total_target_amount": total_target,
            "savings_target_amount": savings_target,
            "deposit_target_amount": deposit_target,
            "start_date": start_date,
            "end_date": end_date
        })

# 더미 찜한 상품 데이터 생성
num_products = 100  # 금융 상품은 100개 있다고 가정
wishlist = []
for user in users:
    product_ids = random.sample(range(1, num_products + 1), random.randint(1, 5))
    for pid in product_ids:
        wishlist.append({
            "user_id": user["user_id"],
            "financial_product_id": pid
        })

# DataFrame으로 변환
df_users = pd.DataFrame(users)
df_goals = pd.DataFrame(goals)
df_wishlist = pd.DataFrame(wishlist)

# 파일 저장
user_path = "/mnt/data/dummy_users.csv"
goal_path = "/mnt/data/dummy_goals.csv"
wishlist_path = "/mnt/data/dummy_wishlist.csv"

df_users.to_csv(user_path, index=False)
df_goals.to_csv(goal_path, index=False)
df_wishlist.to_csv(wishlist_path, index=False)

user_path, goal_path, wishlist_path
