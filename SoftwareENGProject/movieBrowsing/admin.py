from django.contrib import admin
from .models import Profile, TMDBMovie, Theater, Showtime

# Register your models here.
from .models import Profile

admin.site.register(Profile)

admin.site.register(TMDBMovie)

admin.site.register(Theater)

admin.site.register(Showtime)