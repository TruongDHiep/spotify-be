from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'dob', 'is_premium', 'is_online')
    search_fields = ('name', 'email')
    list_filter = ('is_premium', 'is_online')