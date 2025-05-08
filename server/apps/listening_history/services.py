from django.shortcuts import get_object_or_404
from .models import ListeningHistory

class ListeningHistoryService:
    @staticmethod
    def get_listening_history(user_id):
        return ListeningHistory.objects.filter(user_id=user_id)
    
    @staticmethod
    def create_listening_history(user_id, song_id):
        return ListeningHistory.objects.create(user_id=user_id, song_id=song_id)
