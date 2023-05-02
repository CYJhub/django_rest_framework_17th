from rest_framework import routers
from .views import *
from django.urls import path
app_name = 'account'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),  # 로그 아웃
    path('auth/', AuthView.as_view()),  # 인가 (사용자 확인)
    #path('auth/refresh/', TokenRefreshView.as_view()),  # refresh token
];
