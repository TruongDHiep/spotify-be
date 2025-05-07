from django.urls import path
from .views import *

urlpatterns = [
    path('', get_albums, name='get_albums'),
    path('<int:album_id>/', get_album_detail, name='get_album_detail'),
    path('create/', create_album, name='create_album'),
    path('<int:album_id>/update/', update_album, name='update_album'),
    path('<int:album_id>/delete/', delete_album, name='delete_album'),
]