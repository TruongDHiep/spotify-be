from .models import User
from django.core.exceptions import ObjectDoesNotExist
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.hashers import make_password
from django.conf import settings
import secrets

class UserService:
    # Giữ phương thức hiện có
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
    def verify_google_token(token):
        try:
            # Xác minh token Google
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                None
            )
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return None
                
            return {
                'email': idinfo['email'],
                'username': idinfo['email'].split('@')[0],
                'avatar': idinfo.get('picture', ''),
                'name': idinfo.get('name', ''),
            }
        except Exception:
            return None
    
    @staticmethod
    def verify_facebook_token(token):
        try:
            app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
            app_secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET
            
            # Kiểm tra token
            url = f"https://graph.facebook.com/debug_token?input_token={token}&access_token={app_id}|{app_secret}"
            response = requests.get(url)
            data = response.json()
            
            if not data.get('data', {}).get('is_valid'):
                return None
                
            # Lấy thông tin người dùng
            user_info_url = f"https://graph.facebook.com/me?fields=id,name,email,picture&access_token={token}"
            user_info = requests.get(user_info_url).json()
            
            return {
                'email': user_info.get('email'),
                'username': f"fb_{user_info.get('id')}",
                'avatar': user_info.get('picture', {}).get('data', {}).get('url', ''),
                'name': user_info.get('name', ''),
            }
        except Exception:
            return None
    
    @staticmethod
    def get_or_create_social_user(provider, user_data):
        email = user_data.get('email')
        
        # Tìm người dùng theo email
        try:
            user = User.objects.get(email=email)
            return user, False
        except User.DoesNotExist:
            # Tạo người dùng mới
            username = user_data.get('username')
            # Đảm bảo username là duy nhất
            count = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{count}"
                count += 1
                
            # Tạo mật khẩu ngẫu nhiên
            random_password = secrets.token_urlsafe(16)
            
            user = User.objects.create(
                username=username,
                email=email,
                pass_hash=make_password(random_password),
                avatar=user_data.get('avatar', ''),
                dob='2000-01-01',  # Giá trị mặc định
                is_premium=False,
                is_online=True,
            )
            
            return user, True