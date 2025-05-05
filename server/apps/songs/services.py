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
    def update_song(song_id, data, file_upload=None, img_upload=None, mv_upload=None):
        song = get_object_or_404(Song, id=song_id)
        # Upload và xử lý file trước khi cập nhật bản ghi Song
        if file_upload:
            if song.file_upload:  # kiểm tra có file cũ không
                delete_from_s3(song.file_upload)
            file_url = upload_to_s3(file_upload, 'mnm/songfile')
            data['file_upload'] = SongService.timestate_url(file_url)
        if img_upload:
            if song.img:  # kiểm tra có ảnh cũ không
                delete_from_s3(song.img)
            img_url = upload_to_s3(img_upload, 'mnm/songimg')
            data['img'] = SongService.timestate_url(img_url)
        if mv_upload:
            if song.mv and song.mv != "none":  # kiểm tra có MV cũ không
                delete_from_s3(song.mv)
            video_url = upload_to_s3(mv_upload, 'mnm/video')
            data['mv'] = SongService.timestate_url(video_url)
        elif song.mv != "none":
        # Nếu không upload mv mới và mv cũ tồn tại, ta giữ nguyên mv cũ
            pass
        else:
        # Nếu không upload mv mới và mv cũ là "none", gán lại "none"
            data['mv'] = "none"
        # Cập nhật bản ghi Song sau khi đã có đầy đủ thông tin
        for key, value in data.items():
            setattr(song, key, value)
        song.save()
        return song
    
    @staticmethod
    def delete_song(song_id):
        song = get_object_or_404(Song, id=song_id)
        # Xóa file cũ nếu có
        if song.file_upload:
            delete_from_s3(song.file_upload)
        if song.img:
            delete_from_s3(song.img)
        if song.mv and song.mv != "none":
            delete_from_s3(song.mv)
        song.delete()