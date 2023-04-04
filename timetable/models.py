from django.db import models
from board.models import User, School
from core.models import TimestampedModel

class Friend(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Timetable(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=20,default= "시간표")
    semester = models.CharField(max_length=20)
    is_public = models.CharField(max_length= 10)

    def __str__(self):
        return self.name

class Lecture(TimestampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)
    lecture_code = models.CharField(max_length=10)
    professor = models.CharField(max_length=30)
    lecture_time = models.CharField(max_length=30)
    lecture_room = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    grade = models.IntegerField
    credit = models.IntegerField
    capacity = models.IntegerField

    def __str__(self):
        return self.name

class MyLecture(TimestampedModel):
    lecture = models.ForeignKey(Lecture,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name}:{self.lecture.name}'

class Review(TimestampedModel):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    semester = models.CharField(max_length=20)
    content = models.TextField(blank=False)
    star = models.IntegerField
    likeCnt = models.IntegerField

    def __str__(self):
        return f'{self.star}:{self.content}'





