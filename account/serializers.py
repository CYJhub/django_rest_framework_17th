from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School # models.py의 school 사용
        fields = '__all__' # 모든 필드 포함


class UserSerializer(serializers.ModelSerializer):
    school = SchoolSerializer # nested_serializer 사용해서 관계 생성

    class Meta:
        model = User # models.py의 User 사용
        fields = '__all__'  # 모든 필드 포함


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=True,
        write_only=True,
        max_length=30
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    email = serializers.CharField(
        required=True,
        write_only=True,
        max_length=255
    )

    nickname = serializers.CharField(
        required=True,
        write_only=True,
        max_length=255
    )

    class Meta:
        model = User
        fields = ('id','email','password','nickname')

    def save(self, request):
       user = User.objects.create_user(
           id=self.validated_data['id'],
           email=self.validated_data['email'],
           password=self.validated_data['password'],
           nickname=self.validated_data['nickname']
       )
       user.save()

       return user


class LoginSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=True,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'password']

    def validate(self, data):
        id = data.get('id', None)
        password = data.get('password', None)

        if User.objects.filter(id=id).exists():
            user = User.objects.get(id=id)

            if not user.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("user account not exist")

        # RefreshToken 클래스를 사용하여 access token과 refresh token을 발급
        refresh = RefreshToken.for_user(user)

        return {
            'user' : user,
            'id' : id,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }



