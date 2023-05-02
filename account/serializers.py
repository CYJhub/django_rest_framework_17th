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

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



