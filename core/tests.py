from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Review, Favorite
from django.urls import reverse

class MovieModelTest(TestCase):
    def test_string_representation(self):
        movie = Movie(title="The Matrix")
        self.assertEqual(str(movie), "The Matrix")

class ReviewModelTest(TestCase):
    def test_create_review(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        movie = Movie.objects.create(
            title="Inception",
            genre="Sci-Fi",
            release_date="2010-07-16",
            description="A mind-bending thriller."
        )
        review = Review.objects.create(user=user, movie=movie, rating=5, comment="Amazing!")
        self.assertEqual(str(review), "testuser - Inception (5)")

class FavoriteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="favuser", password="testpass")
        self.movie = Movie.objects.create(
            title="Interstellar",
            genre="Sci-Fi",
            release_date="2014-11-07",
            description="Space travel and black holes."
        )
    
    def test_favorite_movie(self):
        self.client.login(username="favuser", password="testpass")
        response = self.client.post(reverse("toggle_favorite", args=[self.movie.id]))
        self.assertEqual(response.status_code, 302)  # redirect after POST
        self.assertTrue(Favorite.objects.filter(user=self.user, movie=self.movie).exists())
