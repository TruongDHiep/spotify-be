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

import json


class PlaylistListView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsSelfOrAdmin]

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
        """Update a playlist partially"""
        playlist = PlaylistService.get_playlist_by_id(pk)
        
        # Parse JSON data from FormData if it exists
        form_data = {}
        if 'data' in request.data:
            try:
                form_data = json.loads(request.data['data'])
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON in data field"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update request.data with parsed data
        serializer = PlaylistSerializer(playlist, data=form_data, partial=True)
        serializer.is_valid(raise_exception=True)
        img_upload = request.FILES.get('img_upload')
        
        updated_playlist = PlaylistService.update_playlist(pk, serializer.validated_data, img_upload)
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
        playlists = PlaylistService.get_playlists_by_user(user_id)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)


