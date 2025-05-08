from django.urls import path
from .views import (
    UserUpdateView,
    UserRegisterView,
    UserLoginView,
    UserIDView,
    UserMeView,
    UserLogoutView,
    ChangePasswordView,
    # SocialLoginView,
    CustomTokenRefreshView,
    UserLogoutView,
    UsernameByIDView,
    GetAllUsersView)

urlpatterns = [
    path('<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('<int:id>', UserIDView.as_view() , name='user-detail'),
    path('username/<int:id>/', UsernameByIDView.as_view(), name='username-by-id'),
    path('getall/', GetAllUsersView.as_view(), name='username-getall'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('<int:id>/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
