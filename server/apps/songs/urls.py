from django.urls import path
from .views import *

urlpatterns = [
    path('', SongListView.as_view(), name='song-list'),  
    path('create', SongListView.as_view(), name='create-song'),
    path('delete/<int:song_id>', SongListView.as_view(), name='delete-song'),
    path('top', TopSongsView.as_view(), name='top-songs'),  
]