from .models import User
from django.core.exceptions import ObjectDoesNotExist
from server.utils import *
import time
    
import requests
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import secrets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import UserSerializer



class UserService:
    @staticmethod
    def timestate_url(url):
        timestamp = int(time.time())
        cache_busting_url = f"{url}?t={timestamp}"
        return cache_busting_url
    
    @staticmethod
    def get_all_users():
        try:
            users = User.objects.all()  # Lấy tất cả người dùng
            return users
        except Exception as e:
            return None
    
    @staticmethod
    def update_user_info(user_id, validated_data, img_upload=None):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

        # Kiểm tra và xử lý img_upload nếu có
        if img_upload:
            img_url = upload_to_s3(img_upload, 'mnm/userAvatars') 
            user.avatar = UserService.timestate_url(img_url)

        # Cập nhật các trường khác từ validated_data
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

    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email), None
        except User.DoesNotExist:
            return None, "Tài khoản không tồn tại"

    @staticmethod
    def authenticate_user(email, password):
        user, error = UserService.get_user_by_email(email)
        if error:
            return None, error
        
        if not check_password(password, user.pass_hash):
            return None, "Sai mật khẩu"
        
        # Cập nhật trạng thái online
        user.is_online = True
        user.save()
        
        return user, None

    @staticmethod
    def register_user(validated_data):
        # Hash mật khẩu
        validated_data['pass_hash'] = make_password(validated_data.pop('password'))
        
        # Tạo người dùng mới
        user = User.objects.create(**validated_data)
        return user

    @staticmethod
    def create_auth_tokens_and_response(user, include_refresh=True):
        # Tạo token JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Tạo response
        response = Response({
            'user': UserSerializer(user).data,
        })
        
        # Set cookies
        if include_refresh:
            UserService.set_auth_cookies(response, access_token, str(refresh))
        else:
            UserService.set_access_token_cookie(response, access_token)
        
        return response

    @staticmethod
    def set_access_token_cookie(response, access_token):
        # Set chỉ access token cookie (thời hạn 5 phút)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=1 * 60,  # 5 phút
            path='/'
        )
        response.data["access"] = access_token
        return response
    
    @staticmethod
    def set_auth_cookies(response, access_token, refresh_token=None):
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=24 * 60 * 60,  # 1 ngày
            path='/'
        )
        response.data["access"] = access_token
        
        # Set refresh token cookie nếu có (thời hạn 7 ngày)
        if refresh_token:
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=7 * 24 * 60 * 60,  # 7 ngày
                path='/'  # Thay đổi path để phù hợp với tất cả requests
            )
        
        return response
    
    @staticmethod
    def refresh_tokens(refresh_token):
        try:
            # Giải mã refresh token để lấy user_id
            refresh = RefreshToken(refresh_token)
            # user_id = refresh.get('user_id')
            # user = User.objects.get(id=user_id)

            # Chỉ làm mới access token, giữ nguyên refresh token cũ
            access_token = str(refresh.access_token)

            response = Response({'message': 'Token refreshed successfully'})
            # Sử dụng set_access_token_cookie thay vì set_auth_cookies
            UserService.set_access_token_cookie(response, access_token)
            return response, None
        except User.DoesNotExist:
            return None, "User not found"
        except TokenError:
            return None, "Invalid refresh token"
    
    @staticmethod
    def change_password(user, old_password, new_password):
        if not check_password(old_password, user.pass_hash):
            return None, "Mật khẩu cũ không đúng."

        user.pass_hash = make_password(new_password)
        user.save()
        return user, None
