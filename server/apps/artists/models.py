from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name