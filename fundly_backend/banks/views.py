# from django.shortcuts import render

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from .utils import split_data
# from .models import Bank, Province, City
# from .serializers import BankSerializer, ProvinceSerializer, CitySerializer

# # Create your views here.
# @api_view(['GET'])
# def save(request):
#     bank_info, province_data, city_data = split_data()
    
#     # 은행 저장
#     for bank in bank_info:
#         if not Bank.objects.filter(name=bank['name']).exists():
#             serializer = BankSerializer(data=bank)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
                
#     # 시, 도 저장
#     for province in province_data:
#         if not Province.objects.filter(name=province['name']).exists():
#             serializer = ProvinceSerializer(data=province)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
                
    
#     # 시군구 저장
#     for cities in city_data:
#         province = Province.objects.get(name=cities['province'])
#         for city in cities['countries']:
#             if not City.objects.filter(name=city['name'], province=province).exists():
#                 serializer = CitySerializer(data=city)
#                 if serializer.is_valid(raise_exception=True):
#                     serializer.save(province=province)
    
#     return Response(status=status.HTTP_201_CREATED)