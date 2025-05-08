from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from apps.artists.views import ArtistViewSet
from apps.albums.views import AlbumViewSet

def home(request):
    return HttpResponse("Welcome to the Spotify Backend API!")

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # This will include the API root
    path('api/users/', include('apps.users.urls')),
    path('api/playlists/', include('apps.playlists.urls')),
    path('api/songs/',include('apps.songs.urls')),
    path('api/genres/', include('apps.genres.urls')),
    path('api/libraries/', include('apps.libraries.urls')),
    path('api/search/', include('apps.search.urls')),
    path('api/playlist_songs/', include('apps.playlist_songs.urls')),
    path('api/chats/', include('apps.chats.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/listening-history/', include('apps.listening_history.urls')),
    path('', home),
]
    