from django.urls import path
from . import views

urlpatterns = [
    path('goals/', views.goals),    # 목표 조회, 생성
    path('goals/<int:goal_pk>/', views.goal_detail),    # 목표 상세 조회, 수정, 삭제
    path('goals/<int:goal_id>/products/<int:product_id>/check-connected/', views.check_product_connected), # 상품이 사용자의 목표와 연결되었는지 확인
    path('wishlist/', views.wish_list),    # 찜하기 전체 조회 / 찜하기 / 삭제
    path('custom/', views.custom_product), # 사용자 설정 상품
    path('custom/goals/<int:goal_pk>/come-from/<str:come_from>/product/<int:product_pk>/', views.custom_detail), 
    path('chatbot/', views.use_finance_chatbot),
]
