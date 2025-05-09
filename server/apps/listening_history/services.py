from django.shortcuts import get_object_or_404
from .models import ListeningHistory
from django.db.models import Max

class ListeningHistoryService:
    @staticmethod
    def get_listening_history(user_id):
        # Lấy các ID của bản ghi mới nhất cho mỗi song
        latest_ids = ListeningHistory.objects.filter(user_id=user_id)\
            .values('song_id')\
            .annotate(latest_id=Max('id'))\
            .values_list('latest_id', flat=True)
        
        # Lấy các bản ghi đầy đủ từ các ID
        return ListeningHistory.objects.filter(id__in=latest_ids)
    
    @staticmethod
    def create_listening_history(user_id, song_id):
        return ListeningHistory.objects.create(user_id=user_id, song_id=song_id)
