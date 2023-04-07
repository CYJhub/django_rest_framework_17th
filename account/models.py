from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from core.models import TimestampedModel
import uuid

class School(TimestampedModel):
    school_name = models.CharField(max_length=100)

    def __str__(self):
        return self.school_name

class UserManager(TimestampedModel):
    # 필수로 필요한 데이터를 선언
    def create_user(self, username, password):
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Password must have and password')

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,TimestampedModel):
    # 기본키
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    id = models.CharField("아이디", max_length= 20)
    password = models.CharField("비밀번호", max_length=128)
    email = models.EmailField("이메일", max_length=128, unique=True)
    nickname = models.CharField("닉네임",max_length=20, unique= True)
    class_of = models.IntegerField("입학연도")
    name = models.CharField("이름",max_length=20)
    join_date = models.DateField("가입일", auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    school_id = models.ForeignKey(School, on_delete=models.PROTECT)

    REQUIRED_FIELDS = ['username']  # 필수로 값을 받아야하는 필드
    USERNAME_FIELD = 'username'
    # custom user 생성 시 필요
    objects = UserManager()

    def __str__(self):
        return self.name


