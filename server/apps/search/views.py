from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from apps.songs.models import Song
from apps.songs.serializers import SongSerializer
from apps.albums.models import Album
from apps.albums.serializers import AlbumSerializer
from apps.artists.models import Artist
from apps.artists.serializers import ArtistSerializer

@api_view(['GET'])
def search_songs(request):
    query = request.GET.get('q', '')
    if not query:
        return Response([], status=status.HTTP_200_OK)
        
    # Tìm bài hát theo tên hoặc lời bài hát
    songs = Song.objects.filter(
        Q(song_name__icontains=query) | 
        Q(description__icontains=query)
    )[:10]  # Giới hạn 10 kết quả
    
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_albums(request):
    query = request.GET.get('q', '')
    if not query:
        return Response([], status=status.HTTP_200_OK)
        
    # Tìm album theo tên hoặc mô tả
    albums = Album.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query)
    )[:10]  # Giới hạn 10 kết quả
    
    serializer = AlbumSerializer(albums, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_artists(request):
    query = request.GET.get('q', '')
    print("Query:", query)
    artists = Artist.objects.filter(Q(name__icontains=query))[:10]
    print("Artists found:", [a.name for a in artists])
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_all(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({
            'songs': [],
            'albums': [],
            'artists': []
        }, status=status.HTTP_200_OK)
    
    # Tìm kiếm tất cả loại đối tượng
    songs = Song.objects.filter(
        Q(song_name__icontains=query) | 
        Q(description__icontains=query)
    )[:5]
    
    albums = Album.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query)
    )[:5]
    
    artists = Artist.objects.filter(
        Q(name__icontains=query) 
    )[:5]
    
    return Response({
        'songs': SongSerializer(songs, many=True).data,
        'albums': AlbumSerializer(albums, many=True).data,
        'artists': ArtistSerializer(artists, many=True).data
    }, status=status.HTTP_200_OK)
