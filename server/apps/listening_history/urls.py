from django.urls import path
from .views import ListeningHistoryView, TopArtistsView

urlpatterns = [
    path('<int:user_id>/', ListeningHistoryView.as_view(), name='listening_history'),
    path('top-artists/', TopArtistsView.as_view(), name='top_artists'), 

]
