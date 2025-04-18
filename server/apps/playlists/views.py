from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Playlist
from .serializers import PlaylistSerializer
from .services import PlaylistService


class PlaylistListView(APIView):
    def get(self, request):
        """Get all playlists or filter by query params"""
        filters = {}
        if 'user_id' in request.query_params:
            filters['id'] = request.query_params['id']
        if 'is_public' in request.query_params:
            filters['is_private'] = request.query_params['is_private'].lower() == 'true'
            
        playlists = PlaylistService.get_playlists(filters)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new playlist"""
        serializer = PlaylistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        playlist = PlaylistService.create_playlist(serializer.validated_data)
        response_serializer = PlaylistSerializer(playlist)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class PlaylistDetailView(APIView):
    def get(self, request, pk):
        """Get a specific playlist"""
        playlist = PlaylistService.get_playlist_by_id(pk)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Update a playlist (complete update)"""
        playlist = PlaylistService.get_playlist_by_id(pk)
        serializer = PlaylistSerializer(playlist, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_playlist = PlaylistService.update_playlist(pk, serializer.validated_data)
        response_serializer = PlaylistSerializer(updated_playlist)
        return Response(response_serializer.data)
    
    def patch(self, request, pk):
        """Update a playlist partially"""
        playlist = PlaylistService.get_playlist_by_id(pk)
        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_playlist = PlaylistService.update_playlist(pk, serializer.validated_data)
        response_serializer = PlaylistSerializer(updated_playlist)
        return Response(response_serializer.data)
    
    def delete(self, request, pk):
        """Delete a playlist"""
        PlaylistService.delete_playlist(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlaylistSongView(APIView):
    def post(self, request, playlist_id, song_id):
        """Add a song to a playlist"""
        playlist = PlaylistService.add_song_to_playlist(playlist_id, song_id)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)
    
    def delete(self, request, playlist_id, song_id):
        """Remove a song from a playlist"""
        playlist = PlaylistService.remove_song_from_playlist(playlist_id, song_id)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)