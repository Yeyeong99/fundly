from django.urls import path
from . import views

urlpatterns = [
    path('save/', views.save_financial_data),                           # 금감원 API 이용 데이터 저장
    path('products/', views.finance_product),                           # 금융 상품 목록 조회 및 생성
    path('products/<str:come_from>/<int:product_pk>/', views.product_detail),           # 상품 상세 조회
    path('show/spot/', views.show_spot_type),    # 현물 데이터 전달
]
