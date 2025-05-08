from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Playlist
from .serializers import PlaylistSerializer
from .services import PlaylistService
from apps.users.models import User 
from apps.libraries.services import LibraryService
from apps.users.authentication import CookieJWTAuthentication
from apps.users.permissions import IsSelfOrAdmin
from rest_framework.pagination import PageNumberPagination



import json

class PlaylistPagination(PageNumberPagination):
    page_size = 10
class PlaylistListView(APIView):
    # authentication_classes = [CookieJWTAuthentication]
    # permission_classes = [IsSelfOrAdmin]

    def get(self, request):
        """Get all playlists or filter by query params"""
        filters = {}
        
        # Lọc theo user_id nếu có
        if 'user_id' in request.query_params:
            filters['user_id'] = request.query_params['user_id']
        
        # Lọc theo is_private nếu có
        if 'is_public' in request.query_params:
            filters['is_private'] = request.query_params['is_public'].lower() != 'true'  # Đảo ngược logic
        
        # Lấy danh sách playlist dựa trên bộ lọc
        playlists = PlaylistService.get_playlists(filters)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)
    
    # def post(self, request):
    #     """Create a new playlist"""
    #     serializer = PlaylistSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     playlist = PlaylistService.create_playlist(serializer.validated_data)
    #     response_serializer = PlaylistSerializer(playlist)
    #     return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def post(self, request):
        """Create a new playlist and add to user library"""
        data = {
            'name':"New Playlist",
            'cover_image':'https://example.com/image.jpg',
            'is_private': False,
            'user_id': request.user.id,
        }
        
        # Create playlist
        playlist = PlaylistService.create_playlist(data)
        
        # Add to user's library (temporarily using userId=1)
        try:
            user = User.objects.get(id=request.user.id)
            LibraryService.addToLibrary(user, 'playlist', playlist.id)
        except Exception as e:
            # Log error but don't fail the playlist creation
            print(f"Failed to add playlist to library: {str(e)}")
        
        # Return response
        response_serializer = PlaylistSerializer(playlist)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class PlaylistDetailView(APIView):
    def get(self, request, pk):
        """Get a specific playlist"""
        playlist = PlaylistService.get_playlist_by_id(pk)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)
    
    
    # def put(self, request, pk, ):
    #     """Update a playlist (complete update)"""
    #     playlist = PlaylistService.get_playlist_by_id(pk)
    #     serializer = PlaylistSerializer(playlist, data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     updated_playlist = PlaylistService.update_playlist(pk, serializer.validated_data,img_upload)
    #     response_serializer = PlaylistSerializer(updated_playlist)
    #     return Response(response_serializer.data)
    

    def patch(self, request, pk):
         playlist = PlaylistService.get_playlist_by_id(pk)
        
         # Lấy và parse JSON từ request.data['data']
         form_data = {}
         if 'data' in request.data:
             form_data = json.loads(request.data['data'])
        
         # Khởi tạo serializer với dữ liệu mới
         serializer = PlaylistSerializer(playlist, data=form_data, partial=True)
         serializer.is_valid(raise_exception=True)
        
         # Lấy file ảnh từ request.FILES
         img_upload = request.FILES.get('img_upload')
        
         # Gọi service để update
         updated_playlist = PlaylistService.update_playlist(pk, serializer.validated_data, img_upload)
        
         # Trả response
         response_serializer = PlaylistSerializer(updated_playlist)
         return Response(response_serializer.data)
        
         
         def delete(self, request, pk):
             """Delete a playlist"""
             PlaylistService.delete_playlist(pk)
             return Response(status=status.HTTP_204_NO_CONTENT)
        
class PlaylistsByUserView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsSelfOrAdmin]
    def get(self, request):
        """Lấy tất cả playlist theo user ID"""
        user_id = request.user.id
        print(user_id)
        playlists = PlaylistService.get_playlists_by_user(user_id)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

class PlaylistWithUserView(APIView):
    def get(self, request):
        data = PlaylistService.get_all_playlists_with_usernames()
        return Response(data)

class AddNewPlaylistView(APIView):
    def post(self, request):
        name = request.data.get("name")
        is_private = request.data.get("is_private", False)
        user_id = request.data.get("user")
        cover_image = request.data.get("cover_image")  # Lấy base64 string từ request.data

        if not name or not cover_image:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id) if user_id else None
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        playlist = Playlist.objects.create(
            name=name,
            is_private=is_private,
            user=user,
            cover_image=cover_image  
        )

        return Response({"message": "Playlist created successfully"}, status=status.HTTP_201_CREATED)

