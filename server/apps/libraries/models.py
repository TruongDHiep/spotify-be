from django.db import models
from apps.users.models import User

class Library(models.Model):
    ITEM_TYPES = [('album', 'Album'), ('song', 'Song'), ('playlist', 'Playlist')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    item_id = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)