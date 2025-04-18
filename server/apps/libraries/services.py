from django.shortcuts import get_object_or_404
from .models import Library
from rest_framework.exceptions import ValidationError
from apps.albums.models import Album
from apps.songs.models import Song
from apps.playlists.models import Playlist
from apps.albums.serializers import AlbumSerializer
from apps.songs.serializers import SongSerializer
from apps.playlists.serializers import PlaylistSerializer


class LibraryService:
    @staticmethod
    def get_libraries_detail(user_id):
        """Get libraries detail by userId (album, playlist, song)"""
        libraries = Library.objects.filter(user=user_id)
        library_items = []

        for library in libraries:
            item_type = library.item_type
            item_id = library.item_id

            try:          
                if item_type == 'playlist':
                    item = get_object_or_404(Playlist, id=item_id)
                    serialized = PlaylistSerializer(item).data
                elif item_type == 'album':
                    item = get_object_or_404(Album, id=item_id)
                    serialized = AlbumSerializer(item).data
                elif item_type == 'song':
                    item = get_object_or_404(Song, id=item_id)
                    serialized = SongSerializer(item).data
                else:
                    continue
            
                library_items.append(serialized)

            except Exception as e:
                print(f"Error getting {item_type} with id {item_id}: {str(e)}")
                continue

        return library_items
        
    @staticmethod
    def addToLibrary(user, item_type, item_id):
        if Library.objects.filter(user=user, item_type=item_type, item_id=item_id).exists():
            raise ValidationError("Item already exists in the library")

        if item_type == 'playlist':
            get_object_or_404(Playlist, id=item_id)
        elif item_type == 'album':
            get_object_or_404(Album, id=item_id)
        elif item_type == 'song':
            get_object_or_404(Song, id=item_id)

        return Library.objects.create(user=user, item_type=item_type, item_id=item_id)
