from django.urls import path, include
from rest_framework import routers
from app import views

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
urlpatterns = []
urlpatterns += router.urls
