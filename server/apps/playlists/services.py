from django.shortcuts import get_object_or_404
from .models import Playlist
from rest_framework.exceptions import ValidationError
from server.utils import *
from ..users.services import UserService
import time
from apps.users.models import User
from django.core.exceptions import ObjectDoesNotExist

class PlaylistService:
    
    @staticmethod
    def get_all_playlists_with_usernames():
        playlists = Playlist.objects.all()
        result = []
        for playlist in playlists:
            username = UserService.get_username_by_id(playlist.user_id)
            result.append({
                "id": playlist.id,
                "name": playlist.name,
                "create_at": playlist.create_at,
                "is_private": playlist.is_private,
                "cover_image": playlist.cover_image,
                "user_id": playlist.user_id,
                "username": username
            })
        return result
    
    @staticmethod
    def timestate_url(url):
        timestamp = int(time.time())
        cache_busting_url = f"{url}?t={timestamp}"
        return cache_busting_url
    
    @staticmethod
    def get_playlists(filters):
        """
        Lấy danh sách playlist dựa trên bộ lọc
        """
        return Playlist.objects.filter(**filters)
        
    @staticmethod
    def get_playlist_by_id(playlist_id):
        """Get a specific playlist by ID"""
        return get_object_or_404(Playlist, id=playlist_id)
    
    @staticmethod
    def get_playlists_by_user(user_id):
        """
        Lấy tất cả playlist của một user cụ thể
        """
        return Playlist.objects.filter(user_id=user_id)
    
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


    
    @staticmethod
    def create_playlist_Admin(data, img_upload=None):
        """Create a new playlistAdmin"""
        user_id = data.pop('user_id', None)
        name_base = data.get('name', 'Playlist')
    
        if not user_id:
            raise ValueError("Playlist phải có user_id.")
    
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError("User không tồn tại.")
    
        count = Playlist.objects.filter(user=user).count()
        data['user'] = user
        data['name'] = f"{name_base} {count + 1}"

        if img_upload:
            img_url = upload_to_s3(img_upload, 'mnm/playlistImgs')
            data['cover_image'] = PlaylistService.timestate_url(img_url)
    
        playlist = Playlist.objects.create(**data)
        return playlist
    
    @staticmethod
    def get_playlist_by_user(user_id):
        """Lấy tất cả playlist của một user"""
        playlists = Playlist.objects.filter(user_id=user_id)
        return playlists