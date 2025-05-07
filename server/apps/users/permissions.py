from rest_framework.permissions import BasePermission

class IsSelfOrAdmin(BasePermission):

    # - has_object_permission: Kiểm tra nếu người dùng là admin hoặc là chính mình
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.id == request.user.id