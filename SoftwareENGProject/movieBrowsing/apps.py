from django.apps import AppConfig


class MoviebrowsingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movieBrowsing'
    
    def ready(self):
        import tmdbsimple as tmdb
        tmdb.API_KEY = '01dbaeff8f72fe91afd5bb7c054fbb15'
