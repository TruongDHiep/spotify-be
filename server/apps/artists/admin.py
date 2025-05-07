from django.contrib import admin
from .models import Artist

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'description')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)