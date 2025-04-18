from django.urls import path
from .views import LibraryListView, LibraryDetailView
urlpatterns = [
    path('', LibraryListView.as_view(), name='library-list'),
    path('detail/', LibraryDetailView.as_view(), name='library-detail'),
]