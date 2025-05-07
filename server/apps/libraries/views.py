from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Library
from .serializers import LibrarySerializer
from .services import LibraryService
from apps.users.authentication import CookieJWTAuthentication
from apps.users.permissions import IsSelfOrAdmin


class LibraryListView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsSelfOrAdmin]
    def get(self, request):
        """Get Library Detail by userId"""
        user_id = request.user.id
        libraries_data = LibraryService.get_libraries_detail(user_id)
        return Response(libraries_data)

class LibraryDetailView(APIView):
    def post(self, request):
        """Add an item to the library"""
        serializer = LibrarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data.get('user') 
        item_type = serializer.validated_data.get('item_type')
        item_id = serializer.validated_data.get('item_id')

        library = LibraryService.addToLibrary(user, item_type, item_id)
        response_serializer = LibrarySerializer(library)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
