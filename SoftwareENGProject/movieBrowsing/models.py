from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class TMDBMovie(models.Model):
    movie_id = models.IntegerField(unique=True, help_text="Enter the unique ID for the movie from TMDB")
    title = models.CharField(max_length=255, help_text="Enter the title of the movie")
    poster_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class Theater(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie = models.ForeignKey(TMDBMovie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    showtime = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.theater.name} on {self.showtime}"