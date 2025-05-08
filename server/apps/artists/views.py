from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import ArtistService
from .serializers import ArtistSerializer
from server.utils import *
import json

@api_view(['GET'])
def get_artists(request):
    """Get a list of artists"""
    artists = ArtistService.get_artists()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_artist_detail(request, artist_id):
    """Get details of a specific artist"""
    artist = ArtistService.get_artist_by_id(artist_id)
    serializer = ArtistSerializer(artist)
    return Response(serializer.data)

@api_view(['POST'])
def create_artist(request):
    form_data = {}
    if 'data' in request.data:
        form_data = json.loads(request.data['data'])

    name = form_data.get('name')
    description = form_data.get('description', '')

    img_upload = request.FILES.get('img_upload')
    avatar_url = ''
    if img_upload:
        avatar_url = upload_to_s3(img_upload, 'artists/images')

    if not name:
        return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

    artist_data = {
        "name": name,
        "description": description,
        "avatar": avatar_url,
    }

    artist = ArtistService.create_artist(artist_data)
    response_serializer = ArtistSerializer(artist)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_artist(request, artist_id):
    """Update an existing artist"""

    # Bóc tách form data từ multipart/form-data
    form_data = {}
    if 'data' in request.data:
        form_data = json.loads(request.data['data'])

    name = form_data.get('name')
    description = form_data.get('description', '')

    # Lấy ảnh từ request
    img_upload = request.FILES.get('img_upload')
    avatar_url = None
    if img_upload:
        avatar_url = upload_to_s3(img_upload, 'artists/images')

    # Tạo dict dữ liệu cập nhật
    update_data = {}

    if name:
        update_data['name'] = name
    if description is not None:
        update_data['description'] = description
    if avatar_url:
        update_data['avatar'] = avatar_url

    # Gọi service để cập nhật
    artist = ArtistService.update_artist(artist_id, update_data)

    # Trả về artist sau khi cập nhật
    response_serializer = ArtistSerializer(artist)
    return Response(response_serializer.data, status=status.HTTP_200_OK)



@api_view(['DELETE'])
def delete_artist(request, artist_id):
    """Delete an artist"""
    ArtistService.delete_artist(artist_id)
    return Response(status=status.HTTP_204_NO_CONTENT)