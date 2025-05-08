from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserUpdateSerializer, UserSerializer, UserLoginSerializer, UserRegisterSerializer
from .services import UserService
from .models import User
from apps.playlists.services import PlaylistService
from apps.libraries.services import LibraryService
from .authentication import CookieJWTAuthentication
from .permissions import IsSelfOrAdmin
from django.db import transaction


class UserMeView(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        try:
            user = request.user
            return Response(UserSerializer(user).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
# Giữ UserUpdateView hiện tại
class UserIDView(APIView):
    def get(self, request, id):
        user = UserService.get_user_by_id(id)
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserUpdateSerializer(user).data)

# Add after CustomTokenRefreshView class
class UserLogoutView(APIView):
    
    def post(self, request):
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    
class UserUpdateView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsSelfOrAdmin]

    def put(self, request, id):
        user = UserService.get_user_by_id(id)
        if not user:
            return Response({"message": "User not found"}, status=404)
        
        self.check_object_permissions(request, user)
        
        # Sử dụng serializer với instance
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Để serializer tự update
            return Response(UserSerializer(user).data)
        
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

# Thêm các view mới
class UserRegisterView(APIView):
    authentication_classes = []  # Không cần xác thực 
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Đã kiểm tra email trong serializer, không cần kiểm tra lại
            try:
                with transaction.atomic():
                    # Đăng ký người dùng
                    user = UserService.register_user(serializer.validated_data.copy())
                    
                    # Tạo playlist yêu thích trực tiếp thông qua service
                    playlist_data = {
                        'name': "Bài hát yêu thích",
                        'cover_image': "https://misc.scdn.co/liked-songs/liked-songs-300.jpg",
                        'is_private': True,
                        'user_id': user.id,
                    }
                    favorite_playlist = PlaylistService.create_playlist(playlist_data)
                    
                    # Thêm playlist vào thư viện người dùng
                    LibraryService.addToLibrary(user, 'playlist', favorite_playlist.id)
                    
                return UserService.create_auth_tokens_and_response(user)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    authentication_classes = []  # Không cần xác thực  # Không cần quyền truy cập
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            user, error = UserService.authenticate_user(email, password)
            if error:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
            return UserService.create_auth_tokens_and_response(user)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(APIView):
    authentication_classes = []  # Không cần xác thực
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Thêm log để debug
        print(f"Received refresh token: {refresh_token[:10]}...")
        
        response, error = UserService.refresh_tokens(refresh_token)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return response

class UserLogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
