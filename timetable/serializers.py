from rest_framework import serializers
from .models import *
from account.serializers import *


class FriendSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Friend
        fields = '__all__'  # 모든 필드 포함


class TimetableSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Timetable
        fields = '__all__'  # 모든 필드 포함


class LectureSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()

    class Meta:
        model = Lecture
        fields = '__all__'  # 모든 필드 포함


class MyLectureSerializer(serializers.ModelSerializer):
    lecture = LectureSerializer()
    user = UserSerializer()
    timetable = TimetableSerializer()

    class Meta:
        model = MyLecture
        fields = '__all__'  # 모든 필드 포함


class ReviewSerializer(serializers.ModelSerializer):
    lecture = LectureSerializer()
    user = UserSerializer()

    class Meta:
        model = Review
        fields = '__all__'  # 모든 필드 포함