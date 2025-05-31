from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts),    # 게시글 목록 조회, 작성
    path('<int:post_pk>/', views.post_detail),    # 게시글 상세, 수정, 삭제
    path('<int:post_pk>/comments/', views.comments),    # 댓글 작성, 조회
    path('comments/<int:comment_pk>/', views.comment_detail),    # 댓글 수정, 삭제, 상세
    path('<int:post_pk>/likes/', views.likes),    # 게시글 좋아요
]
