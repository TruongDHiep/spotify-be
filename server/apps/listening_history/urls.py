from django.urls import path
from .views import ListeningHistoryView

urlpatterns = [
    path('<int:user_id>/', ListeningHistoryView.as_view(), name='listening_history'),
]
