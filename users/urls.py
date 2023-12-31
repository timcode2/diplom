from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, UserCreateAPIView

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', UserCreateAPIView.as_view(), name='user_create')
] + router.urls
