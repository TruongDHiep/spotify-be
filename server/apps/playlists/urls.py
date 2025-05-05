from django.urls import path
from .views import *
urlpatterns = [
    path('', PlaylistListView.as_view(), name='playlist-list'),
    path('<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('user/<int:user_id>/', PlaylistsByUserView.as_view(), name='playlists-by-user')
]