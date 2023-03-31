from django.db import models
from board.models import User, School
from core.models import TimestampedModel

class Friend(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

class Timetable(models.Model):
    name = models.CharField(max_length=20)
    is_public = models.CharField(max_length=10)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

class Lecture(models.Model):
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    lecture_code = models.CharField(max_length=10)
    professor = models.CharField(max_length=30)
    lecture_time = models.CharField(max_length=30)
    lecture_room = models.CharField(max_length=20)
    grade = models. IntegerField
    category = models.CharField(max_length=20)
    credit = models.IntegerField
    capacity = models.IntegerField
    plan_file = models.FileField

class My_lecture(models.Model):
    lecture_id = models.ForeignKey(Lecture,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    timetable_id = models.ForeignKey(Timetable, on_delete=models.CASCADE)

class Review(models.Model):
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    star = models.IntegerField
    semester = models.CharField(max_length=20)
    content = models.TextField()
    likeCnt = models.IntegerField






