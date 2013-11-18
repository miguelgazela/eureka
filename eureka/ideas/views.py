from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from ideas.forms import UserCreationForm, IdeaForm
from ideas.models import Idea
import datetime
from django.utils import timezone

# Create your views here.

def index(request):
    return render(request, 'ideas/index.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'ideas/auth/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('index')
            else:
                return HttpResponse("You're account is disabled")
        else:
            return HttpResponse("Invalid login!")

def logout(request):
    auth_logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'GET':
        return render(request, 'ideas/auth/signup.html')
    elif request.method == 'POST':
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            email = user_form.clean_email()
            user_form.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
        else:
            context = {'form': user_form}
            return render(request, 'ideas/auth/signup.html', context)
            
def addidea(request):
	# Verificar se esta logado
	if request.method == 'GET':	
		return render(request, 'ideas/addidea.html')
	elif request.method == 'POST':
		idea_form = IdeaForm(request.POST)

		if idea_form.is_valid():
			new_idea = idea_form.save(commit=False)
		
			new_idea.user = request.user
			new_idea.created = created=timezone.now()
			new_idea.updated = created=timezone.now()

			new_idea.save()
			#idea_form.save_m2m()	# many2may??
		
			return HttpResponse("Ok, I hope!")	
        """
        else:
            context = {'form': user_form}
            return render(request, 'ideas/auth/signup.html', context)
        """

