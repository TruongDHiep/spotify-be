from django.urls import path
from .views import *

urlpatterns = [
    path('', SongListView.as_view(), name='song-list'),  
    path('create', SongListView.as_view(), name='create-song'),
]