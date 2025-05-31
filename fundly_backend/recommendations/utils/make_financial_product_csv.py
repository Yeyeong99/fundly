import os
import json
import pandas as pd

from django.conf import settings

def safe_str(value):
    return str(value) if value is not None else ""

# JSON 파일 로드
# product_json_file_path = os.path.join(settings.BASE_DIR, 'finance', 'fixtures', 'financialproduct.json')
product_json_file_path = r'C:\Users\SSAFY\Desktop\surin\관통프로젝트\fundly_backend\finance\fixtures\financialproduct.json'

with open(product_json_file_path, "r", encoding="utf-8") as f:
    financial_data = json.load(f)

# 상품 필드만 추출
products = []
for item in financial_data:
    fields = item["fields"]
    product_id = item["pk"]
    combined_text = " ".join([
        safe_str(fields.get("product_name")),
        safe_str(fields.get("special_condition")),
        safe_str(fields.get("join_way")),
        safe_str(fields.get("end_interest_rate")),
        safe_str(fields.get("join_member")),
        safe_str(fields.get("etc_note")),
    ])
    products.append({
        "product_id": product_id,
        "product_type": fields.get("product_type"),
        "join_deny": fields.get("join_deny"),
        "text": combined_text
    })

df_products = pd.DataFrame(products)

# 저장 및 확인
csv_path = r"C:\Users\SSAFY\Desktop\surin\관통프로젝트\fundly_backend\recommendations\fixtures\financial_product_text.csv"
df_products.to_csv(csv_path, index=False)

