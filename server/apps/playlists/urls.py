from django.urls import path
from .views import *
urlpatterns = [
    path('', PlaylistListView.as_view(), name='playlist-list'),
    path('<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('user', PlaylistsByUserView.as_view(), name='playlists-by-user'),

    path('user/<int:user_id>/', PlaylistsByUserView.as_view(), name='playlists-by-user'),
    path('getall/', PlaylistWithUserView.as_view(), name='playlist-with-usernames'),
    path("create/", AddNewPlaylistView.as_view(), name="create-playlist-admin"),
    path('update/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-update'),
]