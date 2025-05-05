from .models import User
from django.core.exceptions import ObjectDoesNotExist
from server.utils import *
import time

class UserService:
    
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
    def update_user_avatar(user_id, img_upload):
        """
        Cập nhật ảnh đại diện (avatar) cho user.
        :param user_id: ID của user cần cập nhật
        :param img_upload: file ảnh upload (ví dụ request.FILES.get('avatar'))
        :return: user instance đã cập nhật hoặc None nếu không tìm thấy
        """
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

        if img_upload:
            img_url = upload_to_s3(img_upload, 'mnm/userimg')  # Thư mục bạn đặt tùy ý
            user.avatar = UserService.timestate_url(img_url)  # Thêm timestamp nếu cần cache-busting
            user.save()

        return user