from django.db import models
from django.conf import settings

# 게시글 모델
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)                   # 작성자
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')    # 좋아요 누른 사용자들
    title = models.CharField(max_length=200)                                                       # 제목
    content = models.TextField()                                                                   # 내용
    category = models.CharField(max_length=10)                                                     # 카테고리
    created_at = models.DateTimeField(auto_now_add=True)                                           # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)                                               # 수정 날짜


# 댓글 모델
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    # 작성자
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')                        # 게시글
    content = models.TextField()                                                    # 내용
    created_at = models.DateTimeField(auto_now_add=True)                            # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)                                # 수정 날짜