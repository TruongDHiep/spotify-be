from django.shortcuts import get_object_or_404
from .models import Playlist
from rest_framework.exceptions import ValidationError
from server.utils import *

import time


class PlaylistService:
    
    @staticmethod
    def timestate_url(url):
        timestamp = int(time.time())
        cache_busting_url = f"{url}?t={timestamp}"
        return cache_busting_url
    
    
    @staticmethod
    def get_playlists(filters):
        """Get playlists with optional filtering"""
        queryset = Playlist.objects.all()
        
        if filters:
            if 'id' in filters:
                queryset = queryset.filter(user_id=filters['id'])
            if 'is_private' in filters:
                queryset = queryset.filter(is_public=filters['is_private'])
                
        return queryset
        
    @staticmethod
    def get_playlist_by_id(playlist_id):
        """Get a specific playlist by ID"""
        return get_object_or_404(Playlist, id=playlist_id)
    
    @staticmethod
    def create_playlist(data):
        """Create a new playlist"""
        # add a number to name
        data['name'] = f"{data['name']} {Playlist.objects.filter(user_id=data['user_id']).count() + 1}"
        playlist = Playlist.objects.create(**data)
        return playlist
    
    @staticmethod
    def update_playlist(playlist_id, data, img_upload):
        """Update an existing playlist"""
        
        playlist = get_object_or_404(Playlist, id=playlist_id)
        if img_upload:
            img_url = upload_to_s3(img_upload, 'mnm/playlistImgs')
            playlist.cover_image = PlaylistService.timestate_url(img_url)
        
        for key, value in data.items():
            setattr(playlist, key, value)
        
        playlist.save()
        return playlist
    
    @staticmethod
    def delete_playlist(playlist_id):
        """Delete a playlist"""
        playlist = get_object_or_404(Playlist, id=playlist_id)
        playlist.delete()
        
    @staticmethod
    def add_song_to_playlist(playlist_id, song_id):
        """Add a song to a playlist"""
        playlist = get_object_or_404(Playlist, id=playlist_id)
        playlist.songs.add(song_id)
        playlist.save()
        return playlist
        
    @staticmethod
    def remove_song_from_playlist(playlist_id, song_id):
        """Remove a song from a playlist"""
        playlist = get_object_or_404(Playlist, id=playlist_id)
        playlist.songs.remove(song_id)
        playlist.save()
        return playlist
    