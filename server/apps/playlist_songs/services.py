from apps.playlist_songs.models import PlaylistSong
from apps.songs.models import Song
from apps.songs.serializers import SongSerializer


class PlaylistService:

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