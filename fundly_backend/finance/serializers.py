from rest_framework import serializers
from .models import FinancialCompany, FinancialProduct, AdditionalProduct, Option, AdditionalOption

# 금융 회사 직렬화 시리얼라이저
class FinancialCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCompany
        fields = '__all__'


# 금융 상품 직렬화 시리얼라이저
class FinancialProductSerializer(serializers.ModelSerializer):

    # 외래 키인 금융회사에 대해 시리얼라이저 적용
    financial_company = FinancialCompanySerializer(read_only=True)

    class Meta:
        model = FinancialProduct
        fields = '__all__'


# 금융 상품 옵션 직렬화 시리얼라이저
class OptionSerializer(serializers.ModelSerializer):

    # 외래 키인 금융 회사에 대해
    financial_company = FinancialCompanySerializer(read_only=True)
    # 외래 키인 금융 상품에 대해 시리얼 라이저 적용
    financial_product = FinancialProductSerializer(read_only=True)

    class Meta:
        model = Option
        fields = '__all__'


# 추가 금융 상품 직렬화 시리얼라이저
class AdditionalProductSerializer(serializers.ModelSerializer):

    # 외래 키인 금융 회사에 대해 시리얼라이저 적용
    financial_company = FinancialCompanySerializer(read_only=True)

    class Meta:
        model = AdditionalProduct
        fields = '__all__'


# 추가 금융 상품 옵션 직렬화
class AdditionalOptionSerializer(serializers.ModelSerializer):

    financial_company = FinancialCompanySerializer(read_only=True)
    # 외래 키인 금융 상품에 대해 시리얼 라이저 적용
    financial_product = AdditionalProductSerializer(read_only=True)

    class Meta:
        model = AdditionalOption
        fields = '__all__'


#-----------------------------------------------------------------------------------------------------------------------------------------------------
# 특정 금융 상품의 옵션 조회 시리얼라이저 (저축 금리 유형, 금리, 기간)
class OptionSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ('id', 'save_type', 'interest_rate', 'max_interest_rate', 'save_month', )


# 특정 추가 금융 상품의 옵션 조회, 생성 시리얼라이저
class AdditionalOptionSimpleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdditionalOption
        fields = ('id', 'save_type', 'interest_rate', 'max_interest_rate', 'save_month', )


# 금융 상품 조회 시리얼라이저 (상품명, 금리, 기간, 찜 여부)
class ProductReadSerializer(serializers.ModelSerializer):

    financial_company = FinancialCompanySerializer(read_only=True)
    options = OptionSimpleSerializer(many=True, read_only=True)    # 역참조

    class Meta:
        model = FinancialProduct
        fields = ('id','financial_company', 'product_name', 'product_type', 'come_from', 'options', )


class AdditionalProductReadSerializer(serializers.ModelSerializer):

    financial_company = FinancialCompanySerializer(read_only=True)
    additional_option = AdditionalOptionSimpleSerializer(many=True, read_only=True)    # 역참조

    class Meta:
        model = AdditionalProduct
        fields = ('id', 'product_name', 'financial_company', 'options', )


# 금융 상품 생성 시리얼라이저 (회사, 상품명, 타입, 옵션)
class AdditionalProductCreateSerializer(serializers.ModelSerializer):

    financial_company_name = serializers.CharField(write_only=True)
    additional_option = AdditionalOptionSimpleSerializer(many=True)    # 역참조

    class Meta:
        model = AdditionalProduct
        fields = ('id', 'product_name', 'product_type', 'join_way', 'end_interest_rate', 'max_limit', 'financial_company_name', 'additional_option', )

    def create(self, validated_data):
        # 1. 회사명으로 금융회사 인스턴스 조회
        company_name = validated_data.pop('financial_company_name')
        options_data = validated_data.pop('options')

        # 2. 없으면 생성하기
        company, _ = FinancialCompany.objects.get_or_create(name=company_name)
        product = AdditionalProduct.objects.create(financial_company=company, **validated_data)

        for option_data in options_data:
            AdditionalOption.objects.create(financial_company=company, **option_data)

        return product
    