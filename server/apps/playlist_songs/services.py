from apps.playlist_songs.models import PlaylistSong
from apps.songs.models import Song
from apps.songs.serializers import SongSerializer
from apps.playlist_songs.models import PlaylistSong
from apps.playlists.models import Playlist
from apps.songs.models import Song
from django.shortcuts import get_object_or_404


class Playlist_SongService:

  @staticmethod
  def get_songs_by_playlist(playlist_id):
      """
      Lấy tất cả bài hát thuộc về một playlist cụ thể
      Sử dụng bảng PlaylistSong để tìm các liên kết
      """
      # Tìm tất cả các bản ghi PlaylistSong có playlist_id tương ứng
      playlist_songs = PlaylistSong.objects.filter(playlist_id=playlist_id)
      
      # Lấy song_id từ các bản ghi PlaylistSong
      song_ids = [item.song_id for item in playlist_songs]
      
      # Lấy các bài hát từ danh sách song_id
      songs = Song.objects.filter(id__in=song_ids)
      
      
      
      return songs
  
  @staticmethod
  def add_song_to_playlist(playlist_id, song_id):
        """
        Thêm bài hát vào playlist
        """
        playlist = get_object_or_404(Playlist, id=playlist_id)
        song = get_object_or_404(Song, id=song_id)

        if PlaylistSong.objects.filter(playlist=playlist, song=song).exists():
            raise ValueError("Song already exists in the playlist")

        playlist_song = PlaylistSong.objects.create(playlist=playlist, song=song)
        return playlist_song
    
  
  @staticmethod
  def remove_song_from_playlist(playlist_id, song_id):
        """
        Xóa một bài hát khỏi playlist
        """
        playlist_song = get_object_or_404(PlaylistSong, playlist_id=playlist_id, song_id=song_id)
        playlist_song.delete()
        return {"message": "Song removed from playlist successfully"}