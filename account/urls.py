from rest_framework import routers
from .views import *
from django.urls import path
app_name = 'account'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
];
