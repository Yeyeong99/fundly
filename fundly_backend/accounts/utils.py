import requests

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

# GOOGLE
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET

# KAKAO
KAKAO_CLIENT_ID = settings.KAKAO_CLIENT_ID

BASE_URL = 'http://127.0.0.1:8000/api/auth/'

User = get_user_model()

# 액세스 토큰 요청 함수
def get_access_token(code, provider):
    redirect_uri = BASE_URL + provider + '/callback/'

    if provider == 'google':
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
    
    elif provider == 'kakao':
        token_url = 'https://kauth.kakao.com/oauth/token'
        data = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "code": code
        }

    response = requests.post(token_url, data=data)
    token_data = response.json()
    print(f'발급 토큰 : {token_data}')
    access_token = token_data.get('access_token')
    return access_token


# 사용자 정보 요청 함수
def get_user_info(access_token, provider):
    if provider == 'google':
        userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'


    elif provider == 'kakao':
        userinfo_url = 'https://kapi.kakao.com/v2/user/me'


    userinfo_response = requests.get(
        userinfo_url,
        headers={'Authorization': f'Bearer {access_token}'}
    )

    userinfo = userinfo_response.json()
    print(f'사용자 정보 : {userinfo}')

    if provider == 'google':
        social_id = userinfo.get('sub')
        email = userinfo.get('email')

    elif provider == 'kakao':
        social_id = userinfo.get('id')
        email = userinfo.get('kakao_account').get('email')

    if not email:
        raise ValueError("No email provided")
    
    return email, social_id


def get_or_create_social_user(provider, social_id, email):
    try:
        user = User.objects.get(provider=provider, social_id=social_id)

    except User.DoesNotExist:
        user = User.objects.create_user(
            username=f"{provider}_{social_id}",
            email=email,
            provider=provider,
            social_id=social_id,
            password=User.objects.make_random_password()
        )
    return user


# JWT 생성 함수
def generate_jwt_for_user(user):

    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }