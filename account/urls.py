from rest_framework import routers
from .views import *
from django.urls import path
app_name = 'account'

urlpatterns = [
    path('signup/', SignupView.as_view()),  # 회원 가입
    path('login/', LoginView.as_view()),  # 로그인
    path('logout/', LogoutView.as_view()),  # 로그 아웃
    path('auth/', AuthView.as_view()),  # 인가
];
