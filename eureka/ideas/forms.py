from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from ideas.models import Idea
from ideas.models import Comment
from taggit.forms import *
from django import forms


ALLOWED_ALIAS = [ "aferreira", "jpgomes", "dviana", "ttavares", "mbarreira",
    "agomes", "arobalo", "ppires", "stavares", "lcosta", "ttrindade",
    "bpinto", "cscosta", "jhenriques", "gdias", "ccarvalheira",
    "afigueiroa", "mcarvalho", "tvieira", "lcouto", "rmrodrigues",
    "rfonte", "dacastro", "imota", "hferrolho", "langelo",
    "dsousa", "amsoliveira", "rleal"
]


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        data = self.cleaned_data['email']

        if data.split('@')[0] not in ALLOWED_ALIAS:
            raise forms.ValidationError("You don't have permission to access this application")
        return data

    class Meta:
        model = User
        fields = ( "username", "email", "password1", "password2")


class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'text', 'tags']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

