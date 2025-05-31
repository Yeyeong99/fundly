from django.urls import path

from . import views

urlpatterns = [
    path('', views.ask_recommendation),    # 추천 요청 및 상품 결과 조회
]
