from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from .models import User
import logging

logger = logging.getLogger(__name__)

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        logger.info("Đang xác thực request")
        # Thử cả hai khả năng tên cookie
        raw_token = request.COOKIES.get('access_token') or request.COOKIES.get('access_token')
        logger.info(f"Cookies: {request.COOKIES}")
        
        if raw_token is None:
            logger.warning("Không tìm thấy token trong cookies")
            return None
            
        try:
            validated_token = self.get_validated_token(raw_token)
            logger.info(f"Token đã được xác thực: {validated_token}")
            
            # Tự triển khai phần lấy user thay vì dùng self.get_user()
            user_id = validated_token.get('user_id')
            if not user_id:
                logger.error("Token không chứa user_id")
                raise AuthenticationFailed('Token không chứa thông tin người dùng')
                
            try:
                user = User.objects.get(id=user_id)
                logger.info(f"Xác thực thành công user ID: {user.id}")
                return user, validated_token
            except User.DoesNotExist:
                logger.error(f"Không tìm thấy user với ID {user_id}")
                raise AuthenticationFailed('User not found')
                
        except Exception as e:
            logger.error(f"Lỗi xác thực: {str(e)}")
            raise