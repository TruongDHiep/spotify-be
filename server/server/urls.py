
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/artists/', include('apps.artists.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/playlists/', include('apps.playlists.urls')),
    path('api/libraries/', include('apps.libraries.urls')),
    
]
