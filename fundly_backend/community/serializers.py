from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Post, Comment
from accounts.serializers import UserSimpleInfoSerializer

# 게시글 일부 직렬화
class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    num_of_likes = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    def get_num_of_likes(self, obj):
        return obj.like_users.count()
    
    def get_created_at(self, obj):
        return obj.created_at.date().isoformat()
    
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = Post
        fields = ('id', 'category', 'title', 'user', 'created_at', 'num_of_likes')


# 게시글 시리얼라이저
class PostSerializer(serializers.ModelSerializer):
    
    # 댓글
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = '__all__'

    # 작성자
    user = serializers.SerializerMethodField()
    # 좋아요
    like_users = UserSimpleInfoSerializer(many=True, read_only=True)
    # 댓글
    comments = CommentDetailSerializer(many=True, read_only=True)    # 읽기 전용, 댓글 개수 0개 이상.
    # 좋아요 개수
    num_of_likes = serializers.SerializerMethodField()
    # 댓글 개수 필드
    num_of_comments = serializers.SerializerMethodField()
    # 로그인한 사용자가 좋아요 했는지 여부
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.username  # 문자열로 반환

    def get_num_of_comments(self, obj):    
        return obj.comments.count()
    
    def get_num_of_likes(self, obj):
        return obj.like_users.count()

    def get_is_liked(self, obj):  # 로그인한 사용자가 좋아요 했는지 여부
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False

# 전체 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    # 게시글 시리얼라이저
    class PostTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ('id', 'title', )

    # 게시글
    post = PostTitleSerializer(read_only=True)
    # 작성자
    user = UserSimpleInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    