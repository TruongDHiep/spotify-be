from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserUpdateSerializer
from .services import UserService
from .models import User
class UserIDView(APIView):
    def get(self, request, id):
        user = UserService.get_user_by_id(id)
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserUpdateSerializer(user).data)

    
class UserUpdateView(APIView):
    def put(self, request, id):
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user = UserService.update_user_info(id, serializer.validated_data)
            if user is None:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(UserUpdateSerializer(user).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsernameByIDView(APIView):
    def get(self, request, id):
        user = UserService.get_username_by_id(id)
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"username": user.username}, status=status.HTTP_200_OK)
    
class GetAllUsersView(APIView):
    def get(self, request):
        users = UserService.get_all_users()
        if users is None or not users:
            return Response({"message": "No users found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Chuyển đổi danh sách người dùng thành dữ liệu dạng JSON qua serializer
        user_data = UserUpdateSerializer(users, many=True).data
        
        # Trả về danh sách người dùng
        return Response(user_data, status=status.HTTP_200_OK)

