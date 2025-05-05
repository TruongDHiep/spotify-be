from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserUpdateSerializer, UserSerializer, UserLoginSerializer, UserRegisterSerializer
from .services import UserService
from .models import User

# Giữ UserUpdateView hiện tại
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

# Thêm các view mới
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Hash mật khẩu trước khi lưu
            validated_data = serializer.validated_data.copy()
            validated_data['pass_hash'] = make_password(validated_data.pop('password'))
            
            # Tạo người dùng mới
            user = User.objects.create(**validated_data)
            
            # Tạo token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            
            try:
                # Tìm user theo username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    # Tìm theo email
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    return Response({'error': 'Tài khoản không tồn tại'}, status=status.HTTP_404_NOT_FOUND)
            
            # Kiểm tra mật khẩu
            if not check_password(password, user.pass_hash):
                return Response({'error': 'Sai mật khẩu'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Tạo token JWT
            refresh = RefreshToken.for_user(user)
            
            # Cập nhật trạng thái online
            user.is_online = True
            user.save()
            
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SocialLoginView(APIView):
    def post(self, request):
        provider = request.data.get('provider', '')
        access_token = request.data.get('access_token', '')
        
        if provider == 'google':
            # Xử lý đăng nhập Google
            user_data = UserService.verify_google_token(access_token)
            if not user_data:
                return Response({'error': 'Token không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
        elif provider == 'facebook':
            # Xử lý đăng nhập Facebook
            user_data = UserService.verify_facebook_token(access_token)
            if not user_data:
                return Response({'error': 'Token không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Không hỗ trợ nhà cung cấp này'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Tìm người dùng hoặc tạo mới
        user, created = UserService.get_or_create_social_user(provider, user_data)
        
        # Tạo JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
