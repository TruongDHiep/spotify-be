from django.db import models
from apps.users.models import User

# Create your models here.
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    avatar = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    cover_image = models.TextField()