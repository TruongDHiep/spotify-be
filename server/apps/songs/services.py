from django.shortcuts import get_object_or_404
from .models import Song
from .models import Artist
from django.db import models
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
    def get_song_by_id(song_id):
        """Get a specific song by ID"""
        return get_object_or_404(Song, id=song_id)
    
    @staticmethod
    def get_song_by_name(song_name):
        """Get a specific song by name"""
        return get_object_or_404(Song, song_name=song_name)

    @staticmethod
    def get_song_by_artist(artist_id):
        """Get all songs where the artist is either the owner or a featured artist."""
        artist = get_object_or_404(Artist, id=artist_id)
        return Song.objects.filter(models.Q(artist_owner=artist) | models.Q(artists=artist)).distinct()

    @staticmethod
    def get_song_by_genre(genre_id):
        """Get all songs by genre"""
        return Song.objects.filter(genre=genre_id).distinct()
    
    @staticmethod
    def get_top_songs(limit=10):
        """Get top songs by play count"""
        return Song.objects.order_by('-play_count')[:limit]
    
    @staticmethod
    def get_songs_by_album(album_id):
        """
        Lấy tất cả bài hát thuộc về một album cụ thể
        """
        return Song.objects.filter(album_id=album_id)

    @staticmethod
    def get_song_bypage(page,pageSize = 8):
        """Get song by page"""
        offset = (page - 1) * pageSize #bài đầu
        limit = offset + pageSize #bài cuối
        query_set = Song.objects.all()[offset:limit]
        return query_set
    
    @staticmethod
    def create_song(data, file, img_upload, mv_upload):
        artists = data.pop("artists", [])  # Lấy artists ra khỏi data 
        # Upload và xử lý file trước khi tạo bản ghi Song
        if file:
            file_url = upload_to_s3(file, 'mnm/songfile')
            data['file_upload'] = SongService.timestate_url(file_url)
        if img_upload:
            img_url = upload_to_s3(img_upload, 'mnm/songimg')
            data['img'] = SongService.timestate_url(img_url)
        if mv_upload:
            video_url = upload_to_s3(mv_upload, 'mnm/video')
            data['mv'] = SongService.timestate_url(video_url)
        else:
            data['mv'] = "none"
        # Tạo bản ghi Song sau khi đã có đầy đủ thông tin
        song = Song.objects.create(**data)
        # Thiết lập quan hệ nhiều-nhiều
        if artists:
            song.artists.set(artists)
        return song    
    
    @staticmethod
    def update_song(song_id, data, artists_data=None, file_upload=None, img_upload=None, mv_upload=None):
        song = Song.objects.get(id=song_id)
        
        # Cập nhật các trường thông thường
        for key, value in data.items():
            setattr(song, key, value)
        
        # Cập nhật artists sử dụng phương thức set()
        if artists_data is not None:
            song.artists.set(artists_data)
        
        # Xử lý upload files
        if file_upload:
            # Xóa file cũ nếu có
            if song.file_upload:
                delete_from_s3(song.file_upload)
            # Upload file mới và thêm timestamp
            file_url = upload_to_s3(file_upload, 'mnm/songfile')
            song.file_upload = SongService.timestate_url(file_url)
        
        if img_upload:
            # Xóa ảnh cũ nếu có
            if song.img:
                delete_from_s3(song.img)
            # Upload ảnh mới và thêm timestamp
            img_url = upload_to_s3(img_upload, 'mnm/songimg')
            song.img = SongService.timestate_url(img_url)
        
        if mv_upload:
            # Xóa video cũ nếu có
            if song.mv and song.mv != "none":
                delete_from_s3(song.mv)
            # Upload video mới và thêm timestamp
            video_url = upload_to_s3(mv_upload, 'mnm/video')
            song.mv = SongService.timestate_url(video_url)
        
        song.save()
        return song
    
    @staticmethod
    def update_play_count(song_id):
        """Update play count for a song"""
        song = get_object_or_404(Song, id=song_id)
        song.play_count += 1
        song.save()
        return song

    @staticmethod
    def delete_song(song_id):
        # song = get_object_or_404(Song, id=song_id)
        # # Xóa file cũ nếu có
        # if song.file_upload:
        #     delete_from_s3(song.file_upload)
        # if song.img:
        #     delete_from_s3(song.img)
        # if song.mv and song.mv != "none":
        #     delete_from_s3(song.mv)
        # song.delete()
        """Toggle song status instead of deleting"""
        song = get_object_or_404(Song, id=song_id)
        # Đảo ngược giá trị status
        song.status = not song.status
        song.save()
        return song