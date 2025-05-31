# import json
# import os
# from django.conf import settings

# # 시군 데이터와 은행 데이터 나누기
# def split_data():
#     json_file = os.path.join(settings.BASE_DIR, 'banks', 'data', 'data.json')

#     with open (json_file, 'r', encoding='utf-8') as f:
#         data = json.load(f)
    
#     map_info = data['mapInfo']
#     bank_info = data['bankInfo']
    
#     bank_data = []
#     province_data = []
#     city_data = []
    
#     for info in map_info:
#         new_info = {}
#         new_info['province'] = info['name']
#         new_info['countries'] = []
#         for city in info['countries']:
#             city_dict = {'name': city}
#             new_info['countries'].append(city_dict)
        
#         province_data.append({'name': new_info['province']})
#         city_data.append(new_info)
        
#     for bank in bank_info:
#         bank_data.append({'name': bank})
        
#     return bank_data, province_data, city_data


# # if __name__ == "__main__":
# #     # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# #     # print(BASE_DIR)
# #     bank_data, province_data, city_data = split_data()
# #     print(bank_data[:2])
# #     print(province_data[:2])
# #     print(city_data[:2])