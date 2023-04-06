from django.urls import path
from . import views
from rest_framework import routers
# from .views import BoardListViewSet

urlpatterns = [
    path('', views.BoardList.as_view()),
    path('<int:pk>/', views.BoardDetail.as_view()),
]
'''
router = routers.DefaultRouter()
router.register(r'board', BoardListViewSet)   # register()함으로써 두 개의 url 생성

urlpatterns = router.urls
'''
