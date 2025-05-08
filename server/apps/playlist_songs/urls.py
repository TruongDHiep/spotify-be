from django.urls import path
from .views import PlaylistSongsListView, RemoveSongFromPlaylistView
urlpatterns = [
    path('<int:playlist_id>', PlaylistSongsListView.as_view(), name='playlist-songs-list'),
    path('<int:playlist_id>/add/<int:song_id>/', PlaylistSongsListView.as_view(), name='add-song-to-playlist'),
    path('<int:playlist_id>/remove/<int:song_id>/', RemoveSongFromPlaylistView.as_view(), name='remove-song-from-playlist'),

]