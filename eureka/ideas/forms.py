from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from ideas.models import Idea
from ideas.models import Comment
from taggit.forms import *
from django import forms

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@junifeup.pt" not in data:
            raise forms.ValidationError("Must be a junifeup.pt address")
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

