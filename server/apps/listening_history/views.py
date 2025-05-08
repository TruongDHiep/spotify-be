from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ListeningHistoryService
from .serializers import ListeningHistorySerializer

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


