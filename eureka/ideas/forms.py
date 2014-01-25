from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from ideas.models import Idea
from ideas.models import Comment
from django.contrib.auth import authenticate
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
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class IdeaForm(ModelForm):
	class Meta:
		model = Idea
		fields = ['title', 'text']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
