from django.db import models

# 금융 회사 모델
class FinancialCompany(models.Model):
    TYPE_CHOICES = [
        ('020000', '은행'),
        ('030300', '저축은행'),
    ]
    company_type = models.CharField(max_length=6,          # 권역 코드
                                    choices=TYPE_CHOICES)
    company_code = models.CharField(max_length=20, unique=True)    # 회사 코드
    company_name = models.CharField(max_length=20, unique=True)    # 회사명
    homepage_url = models.CharField(max_length=200)        # 홈페이지 주소
    phone_number = models.CharField(max_length=20)         # 콜센터 전화번호


# 금융 상품 모델
class FinancialProduct(models.Model):
    TYPE_CHOICES = [
        ('D', '예금'),
        ('S', '적금'),
    ]
    DENY_CHOICES = [
        (1, '제한없음'),
        (2, '서민전용'),
        (3, '일부제한'),
    ]
    financial_company = models.ForeignKey(FinancialCompany, on_delete=models.CASCADE, related_name='financial_product')    # 금융회사
    product_code = models.CharField(max_length=50)                                               # 상품 코드
    published_date = models.CharField(max_length=6)                                      # 공시 제출년월
    product_name = models.CharField(max_length=100)                                      # 상품명
    product_type = models.CharField(max_length=5, choices=TYPE_CHOICES)    # 종류 (D: 예금, S: 적금)
    special_condition = models.TextField(null=True, blank=True)    # 우대 조건
    join_way = models.TextField(null=True, blank=True)    # 가입 방법
    end_interest_rate = models.TextField(null=True, blank=True)    # 만기 후 이자율
    join_deny = models.CharField(max_length=10, choices=DENY_CHOICES)    # 가입 제한
    join_member = models.TextField(null=True, blank=True)    # 가입 대상
    etc_note = models.TextField(null=True, blank=True)    # 기타 유의사항
    max_limit = models.PositiveIntegerField(null=True, blank=True)    # 최고한도
    product_start_date = models.DateField()    # 공시 시작일
    product_end_date = models.DateField(null=True, blank=True)    # 공시 종료일
    submit_date = models.DateTimeField()    # 금융회사 제출일
    come_from = models.CharField(max_length=10, default='original')    # 데이터 출처


# 추가 금융 상품
class AdditionalProduct(models.Model):
    TYPE_CHOICES = [
        ('D', '예금'),
        ('S', '적금'),
    ]
    product_name = models.CharField(max_length=100)    # 상품명
    product_type = models.CharField(max_length=5, choices=TYPE_CHOICES)    # 종류
    financial_company = models.ForeignKey(FinancialCompany, on_delete=models.CASCADE, related_name='additional_product')    # 금융회사
    special_condition = models.TextField(null=True, blank=True)    # 우대조건
    join_way = models.TextField(null=True, blank=True)    # 가입 방법
    end_interest_rate = models.TextField(null=True, blank=True)    # 만기 후 이자율
    join_deny = models.CharField(max_length=10, null=True, blank=True)    # 가입 제한
    join_member = models.TextField(null=True, blank=True)    # 가입 대상
    etc_note = models.TextField(null=True, blank=True)    # 기타 유의사항
    max_limit = models.IntegerField(null=True, blank=True)    # 최고한도
    created_at = models.DateTimeField(auto_now_add=True)    # 생성날짜
    come_from = models.CharField(max_length=10, default='additional')    # 데이터 출처

    
# 금융 상품 옵션
class Option(models.Model):
    SAVE_TYPE_CHOICES = [
        ('S', '단리'),
        ('M', '복리'),
    ]

    REWARD_TYPE_CHOICES = [
        ('S', '정액적립식'),
        ('F', '자유적립식'),
    ]
    financial_company = models.ForeignKey(FinancialCompany, on_delete=models.CASCADE, related_name='options')    # 금융 회사
    financial_product = models.ForeignKey(FinancialProduct, on_delete=models.CASCADE, related_name='options')    # 금융 상품
    save_type = models.CharField(max_length=1, choices=SAVE_TYPE_CHOICES)    # 저축 금리 유형
    reward_type = models.CharField(max_length=1,    # 적립 유형
                                   choices=REWARD_TYPE_CHOICES,
                                   null=True, blank=True)
    save_month = models.IntegerField(null=True, blank=True)    # 저축 기간
    interest_rate = models.FloatField(null=True, blank=True)    # 저축 금리
    max_interest_rate = models.FloatField(null=True, blank=True)    # 최고 우대 금리
    come_from = models.CharField(max_length=10, default='original')    # 데이터 출처


# 사용자로부터 추가된 금융 상품 옵션
class AdditionalOption(models.Model):
    SAVE_TYPE_CHOICES = [
        ('S', '단리'),
        ('M', '복리'),
    ]

    REWARD_TYPE_CHOICES = [
        ('S', '정액적립식'),
        ('F', '자유적립식'),
    ]
    financial_company = models.ForeignKey(FinancialCompany, on_delete=models.CASCADE, related_name='additional_option')    # 금융 회사
    financial_product = models.ForeignKey(AdditionalProduct, on_delete=models.CASCADE, related_name='additional_option')    # 금융 상품
    save_type = models.CharField(max_length=1, choices=SAVE_TYPE_CHOICES)    # 저축 금리 유형
    reward_type = models.CharField(max_length=1,    # 적립 유형
                                   choices=REWARD_TYPE_CHOICES,
                                   null=True, blank=True)
    save_month = models.IntegerField(null=True, blank=True)    # 저축 기간
    interest_rate = models.FloatField(null=True, blank=True)    # 저축 금리
    max_interest_rate = models.FloatField(null=True, blank=True)    # 최고 우대 금리
    come_from = models.CharField(max_length=10, default='additional')    # 데이터 출처