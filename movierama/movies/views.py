from django.contrib.auth.decorators import login_required
from django.forms import ChoiceField, Form, ModelForm, RadioSelect
from django.shortcuts import get_object_or_404, redirect, render
from vote.models import DOWN, UP

from movierama.users.models import User

from .models import Movie


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "description"]


VOTE_CHOICES = [
    ("like", "Like"),
    ("dislike", "Dislike"),
    ("remove", "Remove existing vote"),
]


class VoteForm(Form):
    vote = ChoiceField(choices=VOTE_CHOICES, widget=RadioSelect())


@login_required
def movie_vote(request, pk, template_name="movies/movie_vote_form.html"):
    movie = get_object_or_404(Movie, pk=pk)
    form = VoteForm(request.POST or None)

    # Voting logic
    if form.is_valid():
        cd = form.cleaned_data

        # Remove vote if user already voted before
        if movie.votes.exists(request.user.id, action=UP) or movie.votes.exists(
            request.user.id, action=DOWN
        ):
            movie.votes.delete(request.user.id)

        # Revote according to user's choice
        if cd["vote"] == "like":
            movie.votes.up(request.user.id)
        elif cd["vote"] == "dislike":
            movie.votes.down(request.user.id)
        else:
            pass

        return redirect("movies:vote_movies")
    return render(request, template_name, {"form": form})


@login_required
def movie_list(request, template_name="movies/movie_list.html"):
    movies = Movie.objects.all()
    data = {}
    data["object_list"] = movies
    return render(request, template_name, data)


@login_required
def vote_movies(request, template_name="movies/vote_movies.html"):
    movies = Movie.objects.exclude(user=request.user).all()
    for movie in movies:
        my_vote = "have not voted"
        if movie.votes.exists(request.user.id):
            my_vote = "liked"
        elif movie.votes.exists(request.user.id, action=DOWN):
            my_vote = "disliked"
        movie.my_vote = my_vote

    data = {}
    data["object_list"] = movies
    return render(request, template_name, data)


@login_required
def my_movie_list(request, template_name="movies/my_movie_list.html"):
    movies = Movie.objects.filter(user=request.user).all()
    data = {}
    data["object_list"] = movies
    return render(request, template_name, data)


@login_required
def user_movie_list(request, template_name="movies/user_movie_list.html"):
    user_movies = {}
    users = User.objects.all()

    for user in users:
        movies = Movie.objects.filter(user=user).all()
        user_movies.update({user: movies})

    data = {}
    data["object_list"] = user_movies
    return render(request, template_name, data)


@login_required
def user_vote_list(request, template_name="movies/user_vote_list.html"):
    user_movies = {}
    users = User.objects.all()

    for user in users:
        movies = Movie.votes.all(user.id)
        for movie in movies:
            movie.user_vote = (
                "like" if movie.votes.exists(user.id, action=UP) else "dislike"
            )
        user_movies.update({user: movies})

    data = {}
    data["object_list"] = user_movies
    return render(request, template_name, data)


@login_required
def movie_create(request, template_name="movies/movie_form.html"):
    form = MovieForm(request.POST or None)
    if form.is_valid():
        movie = form.save(commit=False)
        movie.user = request.user
        movie.save()
        return redirect("movies:my_movie_list")
    return render(request, template_name, {"form": form})


@login_required
def movie_update(request, pk, template_name="movies/movie_form.html"):
    if request.user.is_superuser:
        movie = get_object_or_404(Movie, pk=pk)
    else:
        movie = get_object_or_404(Movie, pk=pk, user=request.user)
    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
        form.save()
        return redirect("movies:movie_list")
    return render(request, template_name, {"form": form})


@login_required
def movie_delete(request, pk, template_name="movies/movie_confirm_delete.html"):
    if request.user.is_superuser:
        movie = get_object_or_404(Movie, pk=pk)
    else:
        movie = get_object_or_404(Movie, pk=pk, user=request.user)
    if request.method == "POST":
        movie.delete()
        return redirect("movies:movie_list")
    return render(request, template_name, {"object": movie})
