from django.urls import path

from . import views

app_name = "movies"
urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("my_movies/", views.my_movie_list, name="my_movie_list"),
    path("user_movies/", views.user_movie_list, name="user_movie_list"),
    path("movie_users/", views.movie_user_list, name="movie_user_list"),
    path("user_votes/", views.user_vote_list, name="user_vote_list"),
    path("new/", views.movie_create, name="movie_new"),
    path("edit/<int:pk>/", views.movie_update, name="movie_edit"),
    path("delete/<int:pk>/", views.movie_delete, name="movie_delete"),
    path("vote_movies/", views.vote_movies, name="vote_movies"),
    path("movie_vote/<int:pk>/", views.movie_vote, name="movie_vote"),
]
