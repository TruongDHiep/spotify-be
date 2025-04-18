from rest_framework import serializers
from .models import Library

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'
        read_only_fields = ['id', 'create_at',]