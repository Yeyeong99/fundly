import urllib.parse

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (UserSerializer,
                          UserLoginSerializer, 
                          UserProfileSerializer, 
                          UserSignupSerializer, 
                          UserSimpleInfoSerializer,
                          )
from .utils import get_access_token, get_user_info, generate_jwt_for_user, get_or_create_social_user

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
KAKAO_CLIENT_ID = settings.KAKAO_CLIENT_ID

User = get_user_model()

# 현재 유저 보여주기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# 회원가입하기 - 일반 이메일 가입
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_data = UserLoginSerializer(user).data
            # 토큰 발급
            tokens = generate_jwt_for_user(user)
            refresh = tokens.get('refresh')
            access = tokens.get('access')
            return Response(
                {'user': user_data, 'access': access, 'refresh': refresh},
                status=status.HTTP_201_CREATED
            )


# 기본 로그인
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            print(user)
            user_data = UserLoginSerializer(user).data
            print(user_data)
            refresh = serializer.validated_data['refresh']
            access = serializer.validated_data['access']
            return Response({'user': user_data, 'access': access, 'refresh': refresh}, status=status.HTTP_202_ACCEPTED)
        
    return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


# 소셜 로그인
@api_view(['GET', 'POST'])
def social_login(request, provider):
    redirect_uri = f'http://127.0.0.1:8000/api/auth/{provider}/callback/'

    if provider == 'google':
        client_id = GOOGLE_CLIENT_ID    # 클라이언트 ID 받기
        scope = 'openid email profile'
        response_type = 'code'    # 인가 코드 응답 요청

        google_auth_url = (
            'https://accounts.google.com/o/oauth2/v2/auth?' + 
            urllib.parse.urlencode({
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'response_type': response_type,
                'scope': scope,
                'prompt': 'select_account consent',
                'access_type': 'offline',
            })
        )

        return redirect(google_auth_url)
    
    if provider == 'kakao':
        client_id = KAKAO_CLIENT_ID
        response_type = 'code'
        scope = 'openid'

        kakao_auth_url = (
            'https://kauth.kakao.com/oauth/authorize?' + 
            urllib.parse.urlencode({
                'response_type': response_type,
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'scope': scope,
                'prompt': 'select_account',
            })
        )

        return redirect(kakao_auth_url)


# 회원 탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def signout(request):
    user = request.user
    user.delete()
    return Response({'message': '탈퇴되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    
    
# 콜백 함수
@api_view(['GET', 'POST'])
def callback(request, provider):
    code = request.data.get('code') or request.GET.get('code')
    if not code:
        return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        access_token = get_access_token(code, provider)        # 소셜 로그인 토큰 요청
        print(f'토큰 확인 : {access_token}')
        email, social_id = get_user_info(access_token, provider)        # 사용자 정보 요청
        user = get_or_create_social_user(provider, social_id, email)        # 생성하거나 존재하는 정보 가져오거나
        tokens = generate_jwt_for_user(user)        # JWT 토큰 생성
        
        # 프론트로 리디렉션
        frontend_url = f"http://localhost:5173/login/success?access={tokens['access']}&refresh={tokens['refresh']}&user={email}"
        
        print("토큰 전송")
        
        return redirect(frontend_url)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# 닉네임 설정
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def set_nickname(request):
    user = request.user
    serializer = UserSimpleInfoSerializer(user=user)

    if request.method == 'PATCH':
        username = request.data.get('username')
        user.username = username
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        
# 프로필 조회 + 수정
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 비밀번호 수정
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    if request.method == 'PATCH':
        password = request.data.get('password')
        user.password = password
        user.save()
        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 확인하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_user(request):
    
    user = request.user
    user = User.objects.get(email=user)
    if user.provider == 'google' or user.provider == 'kakao':
        return Response({'message': False})
    
    if user.provider == 'fundly':
        input_password = request.data.get('password')
        
        if not input_password:
            return Response({'error': '비밀번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    
        if user.check_password(input_password):
            return Response({'message': '본인 인증되었습니다.'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': '다시 시도해주세요.'}, status=status.HTTP_400_BAD_REQUEST)


# 처음 가입한 소셜 로그인 사용자인지 확인하기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_first_login(request):
    user = request.user
    user = User.objects.get(email=user)
    if user.created_at != user.updated_at:
        return Response({'message': False})
    else:
        return Response({'message': True})