from django.db import models
from account.models import School, User
from core.models import TimestampedModel

class Board(TimestampedModel):
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)

    category = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Post(TimestampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length= 100, null= False)
    content = models.TextField(blank=False)
    likeCnt = models.IntegerField(default=0)
    scrabCnt = models.IntegerField(default=0)
    commentCnt = models.IntegerField(default=0)
    is_anonymous = models.BooleanField(default=True)
    is_question = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class MyBoard(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.board.name

class Comment(TimestampedModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(blank=False)
    likeCnt = models.IntegerField(default=0)
    is_anonymous = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.content

class Scrap(TimestampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title




