from django.shortcuts import get_object_or_404
from .models import Album
from apps.artists.models import Artist
from rest_framework.exceptions import ValidationError
from server.utils import upload_to_s3, delete_from_s3
import time

class AlbumService:
    @staticmethod
    def timestate_url(url):
        timestamp = int(time.time())
        cache_busting_url = f"{url}?t={timestamp}"
        return cache_busting_url

    @staticmethod
    def get_albums(filters=None):
        """Get a list of albums with optional filtering"""
        if filters:
            return Album.objects.filter(**filters)
        return Album.objects.all()

    @staticmethod
    def get_album_by_id(album_id):
        """Get a specific album by ID"""
        return get_object_or_404(Album, id=album_id)

    @staticmethod
    def create_album(data, img_upload=None):
        """Create a new album with optional image upload"""
        if img_upload:
            img_url = upload_to_s3(img_upload, 'mnm/album')
            data['avatar'] = AlbumService.timestate_url(img_url)
        return Album.objects.create(**data)

    @staticmethod
    def update_album(album_id, data, img_upload=None):
        """Update an existing album with optional image upload"""
        album = get_object_or_404(Album, id=album_id)
        
        # Handle image upload
        if img_upload:
            # Delete old image if exists
            if album.avatar:
                delete_from_s3(album.avatar)
            # Upload new image
            img_url = upload_to_s3(img_upload, 'mnm/album')
            data['avatar'] = AlbumService.timestate_url(img_url)
        
        # Update other fields
        for key, value in data.items():
            setattr(album, key, value)
        album.save()
        return album

    @staticmethod
    def delete_album(album_id):
        """Delete an album and its image from S3"""
        album = get_object_or_404(Album, id=album_id)
        # Delete image from S3 if exists
        if album.avatar:
            delete_from_s3(album.avatar)
        album.delete()

    @staticmethod
    def get_albums_by_artist(artist_id):
        """Get all albums by a specific artist"""
        artist = get_object_or_404(Artist, id=artist_id)
        return Album.objects.filter(artist=artist)