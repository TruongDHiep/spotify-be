from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import ArtistService
from .serializers import ArtistSerializer

@api_view(['GET'])
def get_artists(request):
    """Get a list of artists"""
    artists = ArtistService.get_artists()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_artist_detail(request, artist_id):
    """Get details of a specific artist"""
    artist = ArtistService.get_artist_by_id(artist_id)
    serializer = ArtistSerializer(artist)
    return Response(serializer.data)

@api_view(['POST'])
def create_artist(request):
    """Create a new artist"""
    serializer = ArtistSerializer(data=request.data)
    if serializer.is_valid():
        img_upload = request.FILES.get('img_upload')
        artist = ArtistService.create_artist(serializer.validated_data, img_upload)
        return Response(ArtistSerializer(artist).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_artist(request, artist_id):
    """Update an existing artist"""
    serializer = ArtistSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        img_upload = request.FILES.get('img_upload')
        artist = ArtistService.update_artist(artist_id, serializer.validated_data, img_upload)
        return Response(ArtistSerializer(artist).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_artist(request, artist_id):
    """Delete an artist"""
    ArtistService.delete_artist(artist_id)
    return Response(status=status.HTTP_204_NO_CONTENT)