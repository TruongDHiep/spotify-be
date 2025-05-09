from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ListeningHistoryService
from .serializers import ListeningHistorySerializer
from apps.artists.serializers import ArtistSerializer
from apps.songs.models import Song
from apps.artists.models import Artist
from .models import ListeningHistory
from django.db.models import Count
from apps.users.authentication import CookieJWTAuthentication
from apps.users.permissions import IsSelfOrAdmin


class ListeningHistoryView(APIView):
    def get(self, request, user_id):
        listening_history = ListeningHistoryService.get_listening_history(user_id)
        serializer = ListeningHistorySerializer(listening_history, many=True)
        return Response(serializer.data)
    
    def post(self, request, user_id):
        try:
            song_id = request.data.get('song_id')
            if not song_id:
                return Response(
                    {'error': 'song_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            history = ListeningHistoryService.create_listening_history(
                user_id=user_id,
                song_id=song_id
            )
            serializer = ListeningHistorySerializer(history)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TopArtistsView(APIView):
    def get(self, request):
        authentication_classes = [CookieJWTAuthentication]
        permission_classes = [IsSelfOrAdmin]
        
        user = request.user.id

        # Lấy danh sách bài hát mà user đã nghe, đếm số lần nghe
        song_ids = (
            ListeningHistory.objects.filter(user=user)
            .values('song')
            .annotate(play_count=Count('song'))
            .order_by('-play_count')
        )

        # Lấy danh sách nghệ sĩ từ các bài hát
        artist_ids = (
            Song.objects.filter(id__in=[entry['song'] for entry in song_ids])
            .values_list('artist_owner', flat=True)
            .distinct()
        )

        # Lấy thông tin nghệ sĩ
        artists = Artist.objects.filter(id__in=artist_ids)
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

