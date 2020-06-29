from django.core.validators import validate_comma_separated_integer_list
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Genre(models.Model): 
    name = models.CharField(max_length=20) 


# Create your models here.
class Movie(models.Model):
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    poster_path = models.CharField(max_length=200, null=True)
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=200, null=True)
    original_language = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    vote_average = models.FloatField()
    overview = models.TextField()
    release_date = models.DateField()
    color = models.CharField(validators=[validate_comma_separated_integer_list], max_length=30, blank=True, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    genre_ids = models.ManyToManyField(Genre, related_name='genre_movies', blank=True)
    

class Review(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre_ids = models.ManyToManyField(Genre, related_name='review', blank=True) 
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)