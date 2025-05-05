from django.urls import path
from .views import *

urlpatterns = [
    path('<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('<int:id>', UserIDView.as_view() , name='user-detail'),
]
