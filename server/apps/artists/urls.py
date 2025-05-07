from django.urls import path
from .views import get_artists, get_artist_detail, create_artist, update_artist, delete_artist

urlpatterns = [
    path('', get_artists, name='get_artists'),
    path('<int:artist_id>/', get_artist_detail, name='get_artist_detail'),
    path('create/', create_artist, name='create_artist'),
    path('<int:artist_id>/update/', update_artist, name='update_artist'),
    path('<int:artist_id>/delete/', delete_artist, name='delete_artist'),
]