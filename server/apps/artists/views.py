from rest_framework import viewsets, status
from rest_framework.response import Response
from .services import ArtistService
from .serializers import ArtistSerializer
from .models import Artist

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    
    def get_queryset(self):
        return ArtistService.get_artists()
    
    def retrieve(self, request, *args, **kwargs):
        artist = ArtistService.get_artist_by_id(kwargs['pk'])
        serializer = self.get_serializer(artist)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            artist = ArtistService.create_artist(serializer.validated_data)
            return Response(self.get_serializer(artist).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        artist = ArtistService.get_artist_by_id(kwargs['pk'])
        serializer = self.get_serializer(artist, data=request.data, partial=True)
        if serializer.is_valid():
            artist = ArtistService.update_artist(kwargs['pk'], serializer.validated_data)
            return Response(self.get_serializer(artist).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        ArtistService.delete_artist(kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)