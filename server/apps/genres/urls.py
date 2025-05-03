from django.urls import path
from . import views

urlpatterns = [
    path('', views.GenreListCreateAPIView.as_view(), name='genre-list-create'),
    path('<int:pk>', views.GenreRetrieveUpdateDestroyAPIView.as_view(), name='genre-detail'),
]
