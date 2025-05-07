
from django.contrib import admin
from .models import Album

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'description')
    search_fields = ('title', 'description')
    list_filter = ('release_date', 'artist')
    ordering = ('title',)