from django.contrib import admin
from .models import Movie, Review, Comment, Genre
# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)