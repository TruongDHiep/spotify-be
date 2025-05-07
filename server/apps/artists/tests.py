from django.test import TestCase
from rest_framework.test import APIClient
from .models import Artist
from datetime import date

class ArtistModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            name="Test Artist",
            avatar="http://example.com/avatar.jpg",
            description="Test description"
        )

    def test_artist_creation(self):
        self.assertEqual(self.artist.name, "Test Artist")
        self.assertEqual(self.artist.avatar, "http://example.com/avatar.jpg")
        self.assertEqual(self.artist.description, "Test description")
        self.assertTrue(isinstance(self.artist.created_at, date))

class ArtistAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist_data = {
            "name": "New Artist",
            "avatar": "http://example.com/new_avatar.jpg",
            "description": "New description"
        }
        self.artist = Artist.objects.create(
            name="Test Artist",
            avatar="http://example.com/avatar.jpg",
            description="Test description"
        )

    def test_create_artist(self):
        response = self.client.post('/api/artists/', self.artist_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], self.artist_data['name'])

    def test_get_artist_list(self):
        response = self.client.get('/api/artists/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)