from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from core.models import TimestampedModel
import uuid

class School(models.Model):
    school_name = models.CharField(max_length=100)

    def __str__(self):
        return self.school_name

class User(AbstractBaseUser,TimestampedModel):
    # 기본키
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    id = models.CharField("아이디", max_length= 20)
    password = models.CharField("비밀번호", max_length=128)
    email = models.EmailField("이메일", max_length=128, unique=True)
    profile_image = models.ImageField(null=True)
    nickname = models.CharField("닉네임",max_length=20, unique= True)
    class_of = models.IntegerField("입학연도")
    name = models.CharField("이름",max_length=20)
    join_date = models.DateField("가입일", auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    school_id = models.ForeignKey(School, on_delete=models.PROTECT)

    # 어드민 계정을 만들 때 입력받을 정보 ex) email
    # 사용하지 않더라도 선언이 되어야함
    # USERNAME_FIELD와 비밀번호는 기본적으로 포함되어있음

    REQUIRED_FIELDS = ['username']  # 필수로 값을 받아야하는 필드
    USERNAME_FIELD = 'username'
    # custom user 생성 시 필요
    objects = UserManager()

    def __str__(self):
        return self.name

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    # 일반적으로 선언만 해두고 건들지않는다
    def has_perm(self, perm, obj=None):
        return True

    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    # 일반적으로 선언만 해두고 건들지않는다
    def has_module_perms(self, app_label):
        return True

    # admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin

