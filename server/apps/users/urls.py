from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserUpdateView,
    UserRegisterView,
    UserLoginView,
    SocialLoginView
)

urlpatterns = [
    path('<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('social-login/', SocialLoginView.as_view(), name='social-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]