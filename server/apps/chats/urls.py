# chats/urls.py
from django.urls import path
from .views import ChatWithDeepSeekView

urlpatterns = [
    path("chat/", ChatWithDeepSeekView.as_view(), name="chat_with_deepseek"),
]