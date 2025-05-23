from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, null=True)
    pass_hash = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    gender = models.BooleanField(default=True)
    avatar = models.TextField(default='')
    is_premium = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
