from rest_framework import serializers

from django.contrib.auth import get_user_model

from .utils import generate_jwt_for_user

User = get_user_model()

# 현재 로그인 된 유저를 확인하기 위한 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']  # 필요한 필드만 작성

# 회원 가입을 위한 시리얼라이저
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password1', 'password2', )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 존재하는 이메일입니다.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = User.objects.create_user(password=password, **validated_data)
        return user

# 로그인을 위한 시리얼라이저
class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password', )
        extra_kwargs = {
            'email': {
                'validators': [],    # 유효성 검사 제거하기
                'style': {
                    'input_type': 'email',
                }
            },
            'password': {
                'style': {
                    'input_type': 'password',
                }
            }
        }

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호 입니다.')
        
        else:
            raise serializers.ValidationError("존재하지 않는 사용자 입니다.")
        
        jwt = generate_jwt_for_user(user)
        refresh = jwt.get('refresh')
        access = jwt.get('access')

        data = {
            'user': user,
            'refresh': refresh,
            'access': access,
        }

        return data


# 프로필 시리얼라이저
class UserProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField()
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'birth_date', 'work_type', 'assets', 'salary', 'email',)


# 유저 시리얼라이저 >> 커뮤니티 전용
class UserSimpleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']