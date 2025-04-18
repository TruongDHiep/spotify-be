from django.urls import path
from .views import PlaylistListView, PlaylistDetailView, PlaylistSongView
urlpatterns = [
    path('', PlaylistListView.as_view(), name='playlist-list'),
    path('<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('<int:playlist_id>/songs/<int:song_id>/', PlaylistSongView.as_view(), name='playlist-song'),
]