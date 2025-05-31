from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .utils_company import create_company_data
from .utils_product import create_finance_data
from .serializers import (
                            FinancialCompanySerializer,
                            FinancialProductSerializer,
                            AdditionalProductSerializer,
                            OptionSerializer,
                            AdditionalOptionSerializer,
                            ProductReadSerializer,
                            AdditionalProductCreateSerializer,
                            AdditionalProductReadSerializer,
                        )
from .models import FinancialCompany, FinancialProduct, AdditionalProduct, Option, AdditionalOption

from django.conf import settings
import os
import json

# 금감원 API 활용 데이터 저장하기 >> 이미 저장된 것은 저장되지 않도록 해주기
@api_view(['GET'])
def save_financial_data(request):
    products, options = create_finance_data()
    companys = create_company_data()

    # 금융 회사 저장
    for company in companys:
        if not FinancialCompany.objects.filter(company_code=company['company_code'], company_name=company['company_name']).exists():
            serializer = FinancialCompanySerializer(data=company)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    # 금융 상품 저장
    for product in products:
        # 금융 회사 있는지 확인하기
        try:
            financial_company = FinancialCompany.objects.get(company_code=product['financial_company_id'])
        except FinancialCompany.DoesNotExist:
            continue
        
        # 중복 검사하기
        if FinancialProduct.objects.filter(product_code=product['product_code'], financial_company=financial_company).exists():
            continue
        
        product['financial_company'] = financial_company.id
        serializer = FinancialProductSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            serializer.save(financial_company=financial_company)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # 금융 옵션 저장
    for option in options:
        try:
            financial_company = FinancialCompany.objects.get(company_code=option['financial_company_id'])
        except FinancialCompany.DoesNotExist:
            continue
        
        financial_products = FinancialProduct.objects.filter(product_code=option['financial_product_id'], financial_company=financial_company)

        for financial_product in financial_products:
            # 중복 검사
            if Option.objects.filter(financial_product=financial_product,
                                     financial_company=financial_company,
                                     save_month=option['save_month'],
                                     save_type=option['save_type']).exists():
                continue

            option['financial_company'] = financial_company.id
            option['financial_product'] = financial_product.id

            serializer = OptionSerializer(data=option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(financial_company=financial_company,
                                financial_product=financial_product)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'save': 'completed'}, status=status.HTTP_202_ACCEPTED)


# 금융 상품 목록 조회 및 생성
@api_view(['GET', 'POST'])
def finance_product(request):
    if request.method == 'POST':
        serializer = AdditionalProductCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        # 검색 키워드 받기
        keyword = request.GET.get('keyword')
        # 키워드가 있으면
        if keyword:
            official_product = FinancialProduct.objects.filter(product_name__icontains=keyword)
            additional_product = AdditionalProduct.objects.filter(product_name__icontains=keyword)
        else:
            official_product = FinancialProduct.objects.all()
            additional_product = AdditionalProduct.objects.all()
        
        official_serializer = ProductReadSerializer(official_product, many=True)
        additional_serializer = AdditionalProductReadSerializer(additional_product, many=True)

        return Response({
            'official_products': official_serializer.data,
            'additional_products': additional_serializer.data
        })


# 상품 + 옵션 상세 조회
@api_view(['GET'])
def product_detail(request, come_from, product_pk):

    if come_from == 'additional':
        additional_product = AdditionalProduct.objects.get(pk=product_pk)
        if additional_product:
            options = AdditionalOption.objects.filter(financial_product=additional_product)
            product = additional_product
            product_serializer = AdditionalProductSerializer(product)
            options_serializer = AdditionalOptionSerializer(options, many=True)

            return Response({
                'product': product_serializer.data,
                'options': options_serializer.data
            })
    elif come_from == 'original':
        official_product = FinancialProduct.objects.get(pk=product_pk)
    
        if official_product:
            options = Option.objects.filter(financial_product=official_product)
            product = official_product
            product_serializer = FinancialProductSerializer(product)
            options_serializer = OptionSerializer(options, many=True)
            
            return Response({
                'product': product_serializer.data,
                'options': options_serializer.data
            })
        
    return Response({'error':'상품이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def show_spot_type(resquest):

    gold_json_file = os.path.join(settings.BASE_DIR, 'finance', 'data', 'Gold_prices.json')
    silver_json_file = os.path.join(settings.BASE_DIR, 'finance', 'data', 'Silver_prices.json')
    
    with open(gold_json_file, 'r', encoding='utf-8') as f:
        gold_data = json.load(f)

    with open(silver_json_file, 'r', encoding='utf-8') as f:
        silver_data = json.load(f)
        
    return Response({'gold_data': gold_data,
                     'silver_data': silver_data}, status=status.HTTP_200_OK)