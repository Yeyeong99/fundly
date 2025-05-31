import os
import json
from pathlib import Path

from django.conf import settings

# 쉼표 제거 + 숫자인지 확인 후 float 변환
def clean_to_float(value):
    try:
        return float(str(value).replace(',', ''))
    except ValueError:
        return None  # 이상값은 None 처리


def preprocessing(spot_type):
    
    # 엑셀 데이터 불러오기
    # file_path = os.path.join(settings.BASE_DIR, 'finance', 'data', f'{spot_type}_prices.xlsx') 
    file_path = Path(f"C:/Users/SSAFY/Desktop/surin/관통프로젝트/fundly_backend/finance/data/{spot_type}_prices.xlsx")
    df = pd.read_excel(file_path, sheet_name=f'{spot_type}')

    # 필요한 컬럼만 추출 및 컬럼명 정리
    df = df[['Date', 'Open', 'High', 'Low', 'Close/Last', 'Volume']]
    df.columns = ['date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']

    # 쉼표 제거 + float 변환
    for col in ['open_price', 'high_price', 'low_price', 'close_price', 'volume']:
        df[col] = df[col].apply(clean_to_float)
        df[col] = df[col].astype(str).str.replace(',', '').astype(float)
        
    # 날짜 변경
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df["date"].dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['date'])  # 날짜 오류 있는 행 제거

    # 결측치 제거 및 날짜형 변환
    df = df.dropna()
    
    json_file_path = Path(f"C:/Users/SSAFY/Desktop/surin/관통프로젝트/fundly_backend/finance/data/{spot_type}_prices.json")
    df.to_json(json_file_path, force_ascii=False, indent=4)


def change_json_file(spot_type):
    json_file_path = Path(f"C:/Users/SSAFY/Desktop/surin/관통프로젝트/fundly_backend/finance/data/{spot_type}_prices.json")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    valid_keys = data['date'].keys()
    all_data = []

    for key in valid_keys:
        new_data = {}
        new_data['date'] = data['date'][key]
        new_data['open_price'] = data['open_price'][key]
        new_data['close_price'] = data["close_price"][key]
        new_data['high_price'] = data['high_price'][key]
        new_data['low_price'] = data["low_price"][key]
        new_data['volume'] = data["volume"][key]
        all_data.append(new_data)

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
        


# if __name__ == '__main__':
#     for spot_type in ['Gold', 'Silver']:
#         preprocessing(spot_type)
#         change_json_file(spot_type)