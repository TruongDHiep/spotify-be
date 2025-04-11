from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    pass_hash = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    avatar = models.TextField()
    is_premium = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
