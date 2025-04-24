from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import PlaylistService


# Create your views here.
class PlaylistSongsListView(APIView):
    def get(self, request, playlist_id):
        """Get all songs in a playlist"""
        from apps.songs.serializers import SongSerializer
        
        songs = PlaylistService.get_songs_by_playlist(playlist_id)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)