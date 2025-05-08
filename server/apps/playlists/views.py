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
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsSelfOrAdmin]

    def get(self, request):
        page_no = request.query_params.get('pageNo', 0)
        page_size = request.query_params.get('pageSize', 10)

        filters = {}
        if 'user_id' in request.query_params:
            filters['id'] = request.query_params['user_id']
        if 'is_private' in request.query_params:
            filters['is_private'] = request.query_params['is_private'].lower() == 'true'

        playlists = PlaylistService.get_playlists(filters)
        paginator = PlaylistPagination()
        result_page = paginator.paginate_queryset(playlists, request)
        serializer = PlaylistSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Create a new playlist and add to user library"""
        form_data = {}
        if 'data' in request.data:
            form_data = json.loads(request.data['data'])

        img_upload = request.FILES.get('img_upload')

        # Validate required fields
        if 'user_id' not in form_data:
            return Response({'error': 'Missing user_id'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo playlist
        playlist = PlaylistService.create_playlist(form_data, img_upload)

        # Add to library
        try:
            user = User.objects.get(id=form_data['user_id'])
            LibraryService.addToLibrary(user, 'playlist', playlist.id)
        except Exception as e:
            print(f"Failed to add playlist to library: {str(e)}")

        response_serializer = PlaylistSerializer(playlist)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class PlaylistDetailView(APIView):
    def get(self, request, pk):
        playlist = PlaylistService.get_playlist_by_id(pk)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)

    def patch(self, request, pk):
        playlist = PlaylistService.get_playlist_by_id(pk)
        
        form_data = {}
        if 'data' in request.data:
            form_data = json.loads(request.data['data'])

        serializer = PlaylistSerializer(playlist, data=form_data, partial=True)
        serializer.is_valid(raise_exception=True)

        img_upload = request.FILES.get('img_upload')
        updated_playlist = PlaylistService.update_playlist(pk, serializer.validated_data, img_upload)
        response_serializer = PlaylistSerializer(updated_playlist)
        return Response(response_serializer.data)

    def delete(self, request, pk):
        PlaylistService.delete_playlist(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlaylistsByUserView(APIView):
    def get(self, request, user_id):
        playlists = PlaylistService.get_playlist_by_user(user_id)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

class PlaylistWithUserView(APIView):
    def get(self, request):
        data = PlaylistService.get_all_playlists_with_usernames()
        return Response(data)

class AddNewPlaylistView(APIView):
    def post(self, request):
        form_data = {}
        if 'data' in request.data:
            form_data = json.loads(request.data['data'])

        name = form_data.get("name")
        is_private = form_data.get("is_private", False)
        user_id = form_data.get("user")
        img_upload = request.FILES.get('img_upload')

        if not name or not user_id:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "name": name,
            "is_private": is_private,
            "user_id": user.id
        }

        playlist = PlaylistService.create_playlist_Admin(data, img_upload)
        response_serializer = PlaylistSerializer(playlist)

        return Response(response_serializer.data)

class PlaylistSongsGetbyUserView(APIView):
    def get(self, request, user_id):
        playlists = Playlist.objects.filter(user_id=user_id)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)
