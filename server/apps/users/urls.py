from django.urls import path
from .views import (
    UserUpdateView,
    UserRegisterView,
    UserLoginView,
    UserIDView,
    UserMeView,
    UserLogoutView,
    # SocialLoginView,
    CustomTokenRefreshView
)

urlpatterns = [
    path('<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('<int:id>', UserIDView.as_view() , name='user-detail'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('me/', UserMeView.as_view(), name='user-me'),
    # path('social-login/', SocialLoginView.as_view(), name='social-login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
]
