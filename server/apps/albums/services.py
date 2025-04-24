from django.shortcuts import get_object_or_404
from .models import Album
from rest_framework.exceptions import ValidationError

class AlbumService:
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
    def create_album(data):
        """Create a new album"""
        return Album.objects.create(**data)

    @staticmethod
    def update_album(album_id, data):
        """Update an existing album"""
        album = get_object_or_404(Album, id=album_id)
        for key, value in data.items():
            setattr(album, key, value)
        album.save()
        return album

    @staticmethod
    def delete_album(album_id):
        """Delete an album"""
        album = get_object_or_404(Album, id=album_id)
        album.delete()