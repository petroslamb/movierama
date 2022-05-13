from django.forms import CharField, ChoiceField, Form, ModelForm, RadioSelect, Textarea

from .models import Movie

VOTE_CHOICES = [
    ("like", "Like"),
    ("dislike", "Dislike"),
    ("remove", "Remove existing vote"),
]


class MovieForm(ModelForm):
    description = CharField(widget=Textarea())

    class Meta:
        model = Movie
        fields = ["title", "description"]


class VoteForm(Form):
    vote = ChoiceField(choices=VOTE_CHOICES, widget=RadioSelect())
