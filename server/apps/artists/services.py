from django.shortcuts import get_object_or_404
from .models import Artist

class ArtistService:
    @staticmethod
    def get_artists(filters=None):
        """Get a list of artists with optional filtering"""
        if filters:
            return Artist.objects.filter(**filters)
        return Artist.objects.all()

    @staticmethod
    def get_artist_by_id(artist_id):
        """Get a specific artist by ID"""
        return get_object_or_404(Artist, id=artist_id)

    @staticmethod
    def create_artist(data):
        """Create a new artist"""
        return Artist.objects.create(**data)

    @staticmethod
    def update_artist(artist_id, data):
        """Update an existing artist"""
        artist = get_object_or_404(Artist, id=artist_id)
        for key, value in data.items():
            setattr(artist, key, value)
        artist.save()
        return artist

    @staticmethod
    def delete_artist(artist_id):
        """Delete an artist"""
        artist = get_object_or_404(Artist, id=artist_id)
        artist.delete()