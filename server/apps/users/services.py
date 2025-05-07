from .models import User
from django.core.exceptions import ObjectDoesNotExist
from server.utils import *
import time

class UserService:
    
    @staticmethod
    def get_all_users():
        try:
            users = User.objects.all()  # Lấy tất cả người dùng
            return users
        except Exception as e:
            return None
        
    @staticmethod
    def timestate_url(url):
        timestamp = int(time.time())
        cache_busting_url = f"{url}?t={timestamp}"
        return cache_busting_url
    
    @staticmethod
    def update_user_info(user_id, validated_data):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

        for attr, value in validated_data.items():
            setattr(user, attr, value)

        user.save()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
        return user
    
    @staticmethod
    def get_username_by_id(user_id):
        try:
            user = User.objects.get(id=user_id)
            return user.username
        except ObjectDoesNotExist:
            return None