from rest_framework import serializers
from .models import *


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School # models.py의 school 사용
        fields = '__all__' # 모든 필드 포함


class UserSerializer(serializers.ModelSerializer):
    school = SchoolSerializer # nested_serializer 사용해서 관계 생성

    class Meta:
        model = User # models.py의 User 사용
        fields = '__all__'  # 모든 필드 포함


class RegisterSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ("id", "nickname", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            user = User.objects.create_user(validated_data['id'],
                                            validated_data['nickname'],
                                            validated_data['email'],
                                            validated_data['password'])
            user.save()

            return user

        #이미 존재하는 계정인지 확인
        def validate(self, data):
            user_id = data.get('id', None)

            if User.objects.filter(id=user_id).exists():
                raise serializers.ValidationError("User already exists")
            return data

