from django.conf import settings
from django.db import models
from django.urls import reverse
from vote.models import VoteModel


class Movie(VoteModel, models.Model):
    """
    Stores a single movie, related to :model:`auth.User`.
    """

    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movies:movie_edit", kwargs={"pk": self.pk})
