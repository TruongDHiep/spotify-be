from django.urls import path
from .views import *
urlpatterns = [

    path('<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('user/<int:user_id>/', PlaylistsByUserView.as_view(), name='playlists-by-user'),
    path('getall/', PlaylistWithUserView.as_view(), name='playlist-with-usernames'),
    path("create/", AddNewPlaylistView.as_view(), name="create-playlist-admin"),
    path('update/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-update'),
    path('getplaylistbyUser/<int:user_id>/', PlaylistSongsGetbyUserView.as_view(), name='get-playlist-by-user'),
]