from django.urls import path
from .views import ArtistCreateView, ArtistListView

urlpatterns = [
    path('', ArtistCreateView.as_view(), name='artist-create'),
    path('all/', ArtistListView.as_view(), name='artist-list'),
]
