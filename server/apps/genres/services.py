from django.shortcuts import get_object_or_404
from .models import Genre

class GenreService:
    @staticmethod
    def get_all_genres():
        return Genre.objects.all()

    @staticmethod
    def get_genre_by_id(genre_id):
        return get_object_or_404(Genre, id=genre_id)

    @staticmethod
    def create_genre(data):
        return Genre.objects.create(**data)

    @staticmethod
    def update_genre(genre_id, data):
        genre = get_object_or_404(Genre, id=genre_id)
        for key, value in data.items():
            setattr(genre, key, value)
        genre.save()
        return genre

    # @staticmethod
    # def delete_genre(genre_id):
    #     genre = get_object_or_404(Genre, id=genre_id)
    #     genre.delete()
