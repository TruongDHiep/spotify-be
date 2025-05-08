from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .services import AlbumService
from .serializers import AlbumSerializer
from .models import Album

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    
    def get_queryset(self):
        return AlbumService.get_albums()
    
    def retrieve(self, request, *args, **kwargs):
        album = AlbumService.get_album_by_id(kwargs['pk'])
        serializer = self.get_serializer(album)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            album = AlbumService.create_album(serializer.validated_data)
            return Response(self.get_serializer(album).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        album = AlbumService.get_album_by_id(kwargs['pk'])
        serializer = self.get_serializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            album = AlbumService.update_album(kwargs['pk'], serializer.validated_data)
            return Response(self.get_serializer(album).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        AlbumService.delete_album(kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], url_path='artist/(?P<artist_id>[^/.]+)')
    def by_artist(self, request, artist_id=None):
        try:
            albums = AlbumService.get_albums_by_artist(artist_id)
            serializer = self.get_serializer(albums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

