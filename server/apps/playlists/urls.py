from django.urls import path
from .views import *
urlpatterns = [

    #truonghiep
    path('', PlaylistListView.as_view(), name='playlist-list'),
    path('<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('user', PlaylistsByUserView.as_view(), name='playlists-by-user'),
    path('user/<int:user_id>/', PlaylistsByUserViewAdmin.as_view(), name='playlists-by-user'),
    path('getall/', PlaylistWithUserView.as_view(), name='playlist-with-usernames'),
    path("create/", AddNewPlaylistView.as_view(), name="create-playlist-admin"),
    path('update/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-update'),

    ### minhtriet
    path('Admin/user/<int:pk>/', PlaylistsByUserView.as_view(), name='playlist-songs-by-user'),
    path('Admin/getall/', PlaylistWithUserViewAdmin.as_view(), name='playlist-with-usernames'),
    path("Admin/create/", AddNewPlaylistViewAdmin.as_view(), name="create-playlist-admin"),
    path('Admin/update/<int:pk>/', PlaylistSongsGetbyUserViewAdmin.as_view(), name='playlist-update'),
    path('Admin/getplaylistbyUser/<int:user_id>/', PlaylistSongsGetbyUserViewAdmin.as_view(), name='get-playlist-by-user'),
]
    