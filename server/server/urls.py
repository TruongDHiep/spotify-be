from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Spotify Backend API!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/artists/', include('apps.artists.urls')),
    path('api/albums/', include('apps.albums.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/playlists/', include('apps.playlists.urls')),
    path('api/songs/',include('apps.songs.urls')),
    path('api/genres/', include('apps.genres.urls')),
    path('api/libraries/', include('apps.libraries.urls')),
    path('api/search/', include('apps.search.urls')),
    path('api/playlist_songs/', include('apps.playlist_songs.urls')),
    path('', home), 
]
