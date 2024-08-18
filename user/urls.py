from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from user.views import (
    CreateUserView,
    ManagerUserView
)

urlpatterns = [
    path("user-registration/", CreateUserView.as_view(), name="create"),
    path("my-profile/", ManagerUserView.as_view(), name="manage_user"),
    path("get-token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify-token/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "user"
