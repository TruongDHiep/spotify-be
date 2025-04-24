from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import AlbumService
from .serializers import AlbumSerializer

@api_view(['GET'])
def get_albums(request):
    """Get a list of albums"""
    albums = AlbumService.get_albums()
    serializer = AlbumSerializer(albums, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_album_detail(request, album_id):
    """Get details of a specific album"""
    album = AlbumService.get_album_by_id(album_id)
    serializer = AlbumSerializer(album)
    return Response(serializer.data)

@api_view(['POST'])
def create_album(request):
    """Create a new album"""
    serializer = AlbumSerializer(data=request.data)
    if serializer.is_valid():
        album = AlbumService.create_album(serializer.validated_data)
        return Response(AlbumSerializer(album).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_album(request, album_id):
    """Update an existing album"""
    serializer = AlbumSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        album = AlbumService.update_album(album_id, serializer.validated_data)
        return Response(AlbumSerializer(album).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_album(request, album_id):
    """Delete an album"""
    AlbumService.delete_album(album_id)
    return Response(status=status.HTTP_204_NO_CONTENT)
