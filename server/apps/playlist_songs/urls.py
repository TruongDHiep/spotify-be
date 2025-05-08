from django.urls import path
from .views import PlaylistSongsListView, PlaylistSongsAddMultipleView,PlaylistSongsListViewAdmin
urlpatterns = [
    path('<int:playlist_id>', PlaylistSongsListView.as_view(), name='playlist-songs-list'),
    path('<int:playlist_id>/add/<int:song_id>/', PlaylistSongsListView.as_view(), name='add-song-to-playlist'),
    path('add_multiple/', PlaylistSongsAddMultipleView.as_view(), name="add-multiple-songs-to-playlist"),
    path('<int:playlist_id>/<int:song_id>/', PlaylistSongsListViewAdmin.as_view(), name='playlist-song-detail'),
   
]