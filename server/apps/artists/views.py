from rest_framework import generics
from .models import Artist
from .serializers import ArtistSerializer

class ArtistCreateView(generics.CreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class ArtistListView(generics.ListAPIView): 
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer