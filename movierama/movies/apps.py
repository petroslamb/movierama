from django.apps import AppConfig
from watson import search as watson


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "movierama.movies"

    def ready(self):
        Movie = self.get_model("Movie")
        watson.register(Movie)
