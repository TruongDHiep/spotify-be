from .models import User
from django.core.exceptions import ObjectDoesNotExist
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import secrets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import UserSerializer

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
    
    # # Xác minh token từ Google
    # @staticmethod
    # def verify_google_token(token):
    #     try:
    #         # Xác minh token Google với CLIENT_ID của ứng dụng
    #         idinfo = id_token.verify_oauth2_token(
    #             token, 
    #             google_requests.Request(), 
    #             settings.GOOGLE_OAUTH2_CLIENT_ID
    #         )
            
    #         # Kiểm tra issuer của token
    #         if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
    #             return None
            
    #         # Trả về thông tin người dùng từ token
    #         return {
    #             'email': idinfo['email'],
    #             'username': idinfo['email'].split('@')[0],
    #             'avatar': idinfo.get('picture', ''),
    #             'name': idinfo.get('name', ''),
    #         }
    #     except Exception:
    #         # Trả về None nếu có lỗi
    #         return None
    
    # # Xác minh token từ Facebook
    # @staticmethod
    # def verify_facebook_token(token):
    #     try:
    #         # Lấy thông tin ứng dụng từ settings
    #         app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
    #         app_secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET
            
    #         # Kiểm tra token với Facebook Graph API
    #         url = f"https://graph.facebook.com/debug_token?input_token={token}&access_token={app_id}|{app_secret}"
    #         response = requests.get(url)
    #         data = response.json()
            
    #         # Kiểm tra tính hợp lệ của token
    #         if not data.get('data', {}).get('is_valid'):
    #             return None
            
    #         # Lấy thông tin người dùng từ Facebook
    #         user_info_url = f"https://graph.facebook.com/me?fields=id,name,email,picture&access_token={token}"
    #         user_info = requests.get(user_info_url).json()
            
    #         # Trả về thông tin người dùng
    #         return {
    #             'email': user_info.get('email'),
    #             'username': f"fb_{user_info.get('id')}",
    #             'avatar': user_info.get('picture', {}).get('data', {}).get('url', ''),
    #             'name': user_info.get('name', ''),
    #         }
    #     except Exception:
    #         # Trả về None nếu có lỗi
    #         return None
    
    # # Tìm hoặc tạo người dùng từ đăng nhập xã hội
    # @staticmethod
    # def get_or_create_social_user(provider, user_data):
    #     email = user_data.get('email')
        
    #     # Tìm người dùng theo email
    #     try:
    #         user = User.objects.get(email=email)
    #         return user, False  # Trả về user và flag đã tồn tại
    #     except User.DoesNotExist:
    #         # Tạo người dùng mới nếu chưa tồn tại
    #         name = user_data.get('name', email.split('@')[0])
    #         # Tạo mật khẩu ngẫu nhiên an toàn
    #         random_password = secrets.token_urlsafe(16)
            
    #         # Tạo user mới
    #         user = User.objects.create(
    #             name=name,
    #             email=email,
    #             pass_hash=make_password(random_password),
    #             avatar=user_data.get('avatar', ''),
    #             dob='2000-01-01',  # Giá trị mặc định
    #             is_premium=False,
    #             is_online=True,
    #         )
            
    #         return user, True  # Trả về user và flag đã tạo mới

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
        return user

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
    def set_auth_cookies(response, access_token, refresh_token=None):
        # Set access token cookie (thời hạn 5 phút)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=5 * 60,  # 5 phút
            path='/'
        )
        
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
    def set_token_cookie(response, access_token):
        return UserService.set_auth_cookies(response, access_token)

    @staticmethod
    def refresh_tokens(refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            # Tạo refresh token mới
            new_refresh = RefreshToken.for_user(refresh.get('user'))
            access_token = str(new_refresh.access_token)
            
            response = Response({'message': 'Token refreshed successfully'})
            UserService.set_auth_cookies(response, access_token, str(new_refresh))
            return response, None
        except TokenError:
            return None, "Invalid refresh token"

    # # Xác thực và lấy thông tin người dùng từ đăng nhập xã hội
    # @staticmethod
    # def verify_and_get_social_user(provider, access_token):
    #     # Xác thực token theo nhà cung cấp
    #     if provider == 'google':
    #         user_data = UserService.verify_google_token(access_token)
    #     elif provider == 'facebook':
    #         user_data = UserService.verify_facebook_token(access_token)
    #     else:
    #         return None, "Không hỗ trợ nhà cung cấp này"
        
    #     # Kiểm tra tính hợp lệ của token
    #     if not user_data:
    #         return None, "Token không hợp lệ"
        
    #     # Tìm hoặc tạo người dùng
    #     user, created = UserService.get_or_create_social_user(provider, user_data)
    #     return user, None
