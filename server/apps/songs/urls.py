from django.urls import path
from .views import *

urlpatterns = [
    path('', SongListView.as_view(), name='song-list'),  
    path('create', SongListView.as_view(), name='create-song'),
    path('<int:song_id>/', SongDetailView.as_view(), name='song-detail'),
    path('update/<int:song_id>', SongListView.as_view(), name='update-song'),
    path('delete/<int:song_id>', SongListView.as_view(), name='delete-song'),
    path('top', TopSongsView.as_view(), name='top-songs'),  
    path('page/<int:page>', SongPaginationView.as_view(), name='song-pagination'),
    path('playcount/<int:song_id>', SongPlayCountView.as_view(), name='song-playcount'),
    path('album/<int:album_id>/', SongsByAlbumView.as_view(), name='songs-by-album'),
    path('getallsong/', SongListView.as_view(), name='get-all-songs-playlist'),

    path('artist/<int:artist_id>/', SongsByArtistView.as_view(), name='songs-by-artist'),  # Thêm dòng này
]