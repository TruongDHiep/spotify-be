from django.urls import path
from .views import search_songs, search_albums, search_artists, search_all

urlpatterns = [
    path('songs/', search_songs, name='search-songs'),
    path('albums/', search_albums, name='search-albums'),
    path('artists/', search_artists, name='search-artists'),
    path('', search_all, name='search-all'),
]