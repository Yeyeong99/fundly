from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Count    # 집계함수 모음

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer, PostListSerializer, CommentSerializer
from .models import Post, Comment

User = get_user_model()

# 게시글 목록 조회, 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        user = request.user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):    # 유효성 검사
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 게시글 상세, 수정, 삭제 >> 로그인 필요
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, post_pk):
    post = Post.objects.annotate(num_of_comments=Count('comments'), num_of_likes=Count('like_users')).get(pk=post_pk)
    user = request.user
    
    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    if post.user.id == user.pk:
        if request.method == 'PUT':
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):    # 유효성 검사
                serializer.save()
                return Response(serializer.data)
            
        if request.method == 'DELETE':
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# 특정 게시글의 댓글 작성, 조회
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comments(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    
    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 상세, 수정, 삭제 >> 로그인 필요
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    if comment.user.id == user.pk:
        if request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):    # 유효성 검사
                serializer.save()
                return Response(serializer.data)
            
        if request.method == 'DELETE':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
                

# 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def likes(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user

    if request.method == 'POST':
        if user in post.like_users.all():
            post.like_users.remove(user)
            liked = False
        else:
            post.like_users.add(user)
            liked = True

        return Response({
            'num_of_likes': post.like_users.count(),
            'liked': liked
        })
        
