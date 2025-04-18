from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserUpdateSerializer
from .services import UserService

class UserUpdateView(APIView):
    def put(self, request, id):
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user = UserService.update_user_info(id, serializer.validated_data)
            if user is None:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(UserUpdateSerializer(user).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
