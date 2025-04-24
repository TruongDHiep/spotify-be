from django.shortcuts import get_object_or_404
from .models import Song
from server.utils import *

import time

class SongService:
    @staticmethod
    def timestate_url(url):
        timestamp = int(time.time())
        cache_busting_url = f"{url}?t={timestamp}"
        return cache_busting_url

    @staticmethod
    def get_songs():
        query_set = Song.objects.all()
        return query_set
    
    @staticmethod
    def get_song_bypage(page,pageSize = 10):
        """Get song by page"""
        offset = (page - 1) * pageSize #bài đầu
        limit = offset + pageSize #bài cuối
        query_set = Song.objects.all()[offset:limit]
        return query_set
    
    @staticmethod
    def create_song(data,file_upload,img_upload,mv_upload):
        artists = data.pop("artists", [])  # Lấy artists ra khỏi data
        song = Song.objects.create(**data)
        if artists:
            song.artists.set(artists)
        # Upload file mp3
        if file_upload:
            file_url = upload_to_s3(file_upload, 'mnm/songfile')
            data['file_upload'] = SongService.timestate_url(file_url)
        # Upload ảnh bài hát
        if img_upload:
            img_url = upload_to_s3(img_upload, 'mnm/songimg')
            data['img'] = SongService.timestate_url(img_url)
        # Upload video
        if mv_upload:
            video_url = upload_to_s3(mv_upload, 'mnm/video')
            data['mv'] = SongService.timestate_url(video_url)
        else:
            data['mv'] = "none"
        song = Song.objects.create(**data)
        return song
    