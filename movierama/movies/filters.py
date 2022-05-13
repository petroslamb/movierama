import django_filters

from .models import Movie


class MovieUserFilter(django_filters.FilterSet):
    class Meta:
        model = Movie
        fields = ["user"]
