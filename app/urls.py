from django.urls import path, include
from rest_framework import routers
from app import views

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet)
router.register(r"accounts", views.AccountViewSet)
router.register(r"orders", views.OrderViewSet)
router.register(r"products", views.ProductViewSet)
urlpatterns = [
    path("accounts/transfer", views.AccountViewSet.as_view({"post": "transfer"})),
    # Other URL patterns
]
urlpatterns += router.urls
