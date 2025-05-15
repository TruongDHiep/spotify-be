from django.shortcuts import get_object_or_404
from .models import Artist
from server.utils import upload_to_s3, delete_from_s3
import time

class ArtistService:
    @staticmethod
    def timestate_url(url):
        timestamp = int(time.time())
        cache_busting_url = f"{url}?t={timestamp}"
        return cache_busting_url

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
    def create_artist(data, img_upload=None):
        """Create a new artist with optional image upload"""
        if img_upload:
            img_url = upload_to_s3(img_upload, 'mnm/artist')
            data['avatar'] = ArtistService.timestate_url(img_url)
        return Artist.objects.create(**data)

    @staticmethod
    def update_artist(artist_id, data, img_upload=None):
        """Update an existing artist with optional image upload"""
        artist = get_object_or_404(Artist, id=artist_id)
        
        # Handle image upload
        if img_upload:
            # Delete old image if exists
            if artist.avatar:
                delete_from_s3(artist.avatar)
            # Upload new image
            img_url = upload_to_s3(img_upload, 'mnm/artist')
            data['avatar'] = ArtistService.timestate_url(img_url)
        
        # Update other fields
        for key, value in data.items():
            setattr(artist, key, value)
        artist.save()
        return artist

    @staticmethod
    def delete_artist(artist_id):
        """Delete an artist and their image from S3"""
        artist = get_object_or_404(Artist, id=artist_id)
        # Delete image from S3 if exists
        if artist.avatar:
            delete_from_s3(artist.avatar)
        artist.delete()