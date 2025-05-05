from django.urls import path
from .views import PlaylistListView, PlaylistDetailView
urlpatterns = [
    path('', PlaylistListView.as_view(), name='playlist-list'),
    path('<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail')
]