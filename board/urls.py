from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardList, name='board'),
    path('<int:question_id>/', views.BoardDetail, name='detail'),
]