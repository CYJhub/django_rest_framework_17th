from rest_framework import serializers
from .models import *
from account.serializers import *

class BoardSerializer(serializers.ModelSerializer):
    school_id = SchoolSerializer

    class Meta:
        model = Board #  models.py의 board 사용
        fields = '__all__' # 모든 필드 포함

class PostSerializer(serializers.ModelSerializer):
    board = BoardSerializer()
    user = UserSerializer()

    class Meta:
        model = Post #  models.py의 post 사용
        fields = '__all__' # 모든 필드 포함

class MyBoardSerializer(serializers.ModelSerializer):
    board = BoardSerializer()
    user = UserSerializer()

    class Meta:
        model = MyBoard #  models.py의 mypost 사용
        fields = '__all__' # 모든 필드 포함

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    user = UserSerializer()
    # parent_comment = CommentSerializer()

    class Meta:
        model = Comment #  models.py의 comment 사용
        fields = '__all__' # 모든 필드 포함

class InCommentSerializer(serializers.ModelSerializer):
    parent_comment = CommentSerializer()

    class Meta:
        model = Comment
        fields = '__all__'  # 모든 필드 포함

class ScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrap #  models.py의 scrap 사용
        fields = '__all__' # 모든 필드 포함