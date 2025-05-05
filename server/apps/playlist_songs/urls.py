from django.urls import path
from .views import PlaylistSongsListView
urlpatterns = [
    path('<int:playlist_id>', PlaylistSongsListView.as_view(), name='playlist-songs-list'),
    path('<int:playlist_id>/add/<int:song_id>/', PlaylistSongsListView.as_view(), name='add-song-to-playlist'),

]